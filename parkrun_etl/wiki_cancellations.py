import json
import re
import time

import requests
from bs4 import BeautifulSoup

from .http_headers import headers
from .time_utils import now

WIKI_CANCELLATIONS_PAGE = 'Cancellations/Global'
WIKI_API_URL = 'https://wiki.parkrun.com/api.php'
WIKI_CANCELLATIONS_INDEX_URL = (
    'https://wiki.parkrun.com/index.php/Cancellations/Global')
_CANCELLATION_DATE_CELL = re.compile(r'^\d{4}-\d{2}-\d{2}$')


def _cancellations_html_looks_like_waf(html):
    '''Detect AWS WAF / bot interstitial HTML (HTTP 200 but not article content).'''
    if not html:
        return True
    if 'Human Verification' in html and 'awswaf.com' in html:
        return True
    if 'captcha-container' in html and 'AwsWafIntegration' in html:
        return True
    return False


def parse_global_cancellations_table(html):
    '''
    Rows from the Global cancellations wikitable: five text columns.
    Skips the header row and any row whose first cell is not YYYY-MM-DD.
    '''
    soup = BeautifulSoup(html, 'html.parser')
    table = (
        soup.select_one('table.wikitable.sortable')
        or soup.select_one('table.wikitable'))
    if not table:
        return []
    rows = []
    for tr in table.find_all('tr'):
        cells = tr.find_all('td')
        if len(cells) < 5:
            continue
        row = [cells[i].get_text(strip=True) for i in range(5)]
        if not _CANCELLATION_DATE_CELL.match(row[0]):
            continue
        rows.append(row)
    return rows


def fetch_cancellations_wiki_html():
    '''
    Prefer MediaWiki action=parse (article HTML only); fall back to index.php
    and scope to #mw-content-text table.wikitable.
    Returns (html_fragment_to_store, source_label).
    '''
    api_params = {
        'action': 'parse',
        'page': WIKI_CANCELLATIONS_PAGE,
        'prop': 'text',
        'formatversion': '2',
        'format': 'json',
    }
    for attempt in range(10):
        api_response = requests.get(
            WIKI_API_URL,
            params=api_params,
            headers=headers,
            timeout=60)
        if api_response.status_code != 200:
            print(now(), 'wiki API', api_response.status_code,
                  '- waiting 10s to retry', attempt)
            time.sleep(10)
            continue
        try:
            payload = api_response.json()
        except json.JSONDecodeError:
            print(now(), 'wiki API JSON decode error, retry', attempt)
            time.sleep(10)
            continue
        if 'error' in payload:
            print(now(), 'wiki API error', payload['error'], '- trying index URL')
            break
        parse_block = payload.get('parse') or {}
        text_block = parse_block.get('text')
        if isinstance(text_block, dict) and '*' in text_block:
            html = text_block['*']
        elif isinstance(text_block, str):
            html = text_block
        else:
            print(now(), 'wiki API unexpected parse.text shape, fallback')
            break
        if _cancellations_html_looks_like_waf(html):
            print(now(), 'wiki API body looks like WAF challenge, fallback')
            break
        if 'wikitable' not in html:
            print(now(), 'wiki API parse text has no wikitable, fallback')
            break
        return html, 'api'

    print(now(), 'fetching cancellations via index.php (fallback)')
    for attempt in range(10):
        index_response = requests.get(
            WIKI_CANCELLATIONS_INDEX_URL,
            headers=headers,
            timeout=60)
        if index_response.status_code != 200:
            print(now(), index_response, '- waiting 10s to retry')
            time.sleep(10)
            continue
        full_html = index_response.text
        if _cancellations_html_looks_like_waf(full_html):
            print(now(), 'index.php WAF challenge, retry', attempt)
            time.sleep(10)
            continue
        soup = BeautifulSoup(full_html, 'html.parser')
        content = soup.select_one('#mw-content-text')
        if content:
            table = (
                content.select_one('table.wikitable.sortable')
                or content.select_one('table.wikitable'))
            if table:
                return str(table), 'index_scoped'
        if 'wikitable' in full_html:
            return full_html, 'index_full'
        print(now(), 'index.php: no wikitable found, retry', attempt)
        time.sleep(10)

    raise RuntimeError(
        'Failed to load Cancellations/Global from wiki (API and index fallback)')
