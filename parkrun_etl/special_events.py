"""Fetch and parse parkrun special-events HTML (Christmas/NYD etc.)."""
import json

import requests
from bs4 import BeautifulSoup
from html_table_extractor.extractor import Extractor


def load_special_events(fetch_updates, headers, now_fn):
    special_events = []
    if not fetch_updates:
        return special_events

    # Australia
    if fetch_updates:
        se_au = requests.get('https://www.parkrun.com.au/special-events',
                             headers=headers,
                             timeout=10).text
        with open('_data/special_events/au.html',
                  'wt',
                  encoding='utf-8',
                  newline='') as f:
            f.write(se_au)
            print(now_fn(), "_data/special_events/au.html saved")

    with open('_data/special_events/au.html', 'r', encoding='utf-8', newline='\n') as f:
        soup = BeautifulSoup(f, 'html.parser')

        extractor = Extractor(soup)
        extractor.parse()
        se_au_table = extractor.return_list()
        se_au_table.pop(0)

    # Canada
    if fetch_updates:
        se_ca = requests.get('https://www.parkrun.ca/special-events',
                             headers=headers,
                             timeout=10).text
        with open('_data/special_events/ca.html',
                  'wt',
                  encoding='utf-8',
                  newline='') as f:
            f.write(se_ca)
            print(now_fn(), "_data/special_events/ca.html saved")

    with open('_data/special_events/ca.html', 'r', encoding='utf-8', newline='\n') as f:
        soup = BeautifulSoup(f, 'html.parser')

        extractor = Extractor(soup)
        extractor.parse()
        se_ca_table = extractor.return_list()
        se_ca_table.pop(0)

    # Denmark
    if fetch_updates:
        se_dk = requests.get('https://www.parkrun.dk/special-events',
                             headers=headers,
                             timeout=10).text
        with open('_data/special_events/dk.html', 'wt', encoding='utf-8', newline='') as f:
            f.write(se_dk)
            print(now_fn(), "_data/special_events/dk.html saved")

    with open('_data/special_events/dk.html', 'r', encoding='utf-8', newline='\n') as f:
        soup = BeautifulSoup(f, 'html.parser')

        extractor = Extractor(soup)
        extractor.parse()
        se_dk_table = extractor.return_list()
        se_dk_table.pop(0)

    # Finland
    if fetch_updates:
        se_fi = requests.get('https://www.parkrun.fi/special-events',
                             headers=headers,
                             timeout=10).text
        with open('_data/special_events/fi.html', 'wt', encoding='utf-8', newline='') as f:
            f.write(se_fi)
            print(now_fn(), "_data/special_events/fi.html saved")

    with open('_data/special_events/fi.html', 'r', encoding='utf-8', newline='\n') as f:
        soup = BeautifulSoup(f, 'html.parser')

        extractor = Extractor(soup)
        extractor.parse()
        se_fi_table = extractor.return_list()
        se_fi_table.pop(0)

    # France
    if fetch_updates:
        se_fr = requests.get('https://www.parkrun.fr/special-events',
                             headers=headers,
                             timeout=10).text
        with open('_data/special_events/fr.html',
                  'wt',
                  encoding='utf-8',
                  newline='') as f:
            f.write(se_fr)
            print(now_fn(), "_data/special_events/fr.html saved")

    with open('_data/special_events/fr.html',
              'r',
              encoding='utf-8',
              newline='\n') as f:
        soup = BeautifulSoup(f, 'html.parser')

        extractor = Extractor(soup)
        extractor.parse()
        se_fr_table = extractor.return_list()
        se_fr_table.pop(0)

    # Germany
    if fetch_updates:
        se_de = requests.get('https://www.parkrun.com.de/special-events',
                             headers=headers,
                             timeout=10).text
        with open('_data/special_events/de.html',
                  'wt',
                  encoding='utf-8',
                  newline='') as f:
            f.write(se_de)
            print(now_fn(), "_data/special_events/de.html saved")

    with open('_data/special_events/de.html',
              'r',
              encoding='utf-8',
              newline='\n') as f:
        soup = BeautifulSoup(f, 'html.parser')

        extractor = Extractor(soup)
        extractor.parse()
        se_de_table = extractor.return_list()
        se_de_table.pop(0)

    # Ireland
    if fetch_updates:
        se_ie = requests.get('https://www.parkrun.ie/special-events',
                             headers=headers,
                             timeout=10).text
        with open('_data/special_events/ie.html',
                  'wt',
                  encoding='utf-8',
                  newline='') as f:
            f.write(se_ie)
            print(now_fn(), "_data/special_events/ie.html saved")

    with open('_data/special_events/ie.html',
              'r',
              encoding='utf-8',
              newline='\n') as f:
        soup = BeautifulSoup(f, 'html.parser')

        extractor = Extractor(soup)
        extractor.parse()
        se_ie_table = extractor.return_list()
        se_ie_table.pop(0)

    # Italy
    if fetch_updates:
        se_it = requests.get('https://www.parkrun.it/special-events',
                             headers=headers,
                             timeout=10).text
        with open('_data/special_events/it.html',
                  'wt',
                  encoding='utf-8',
                  newline='') as f:
            f.write(se_it)
            print(now_fn(), "_data/special_events/it.html saved")

    with open('_data/special_events/it.html',
              'r',
              encoding='utf-8',
              newline='\n') as f:
        soup = BeautifulSoup(f, 'html.parser')

        extractor = Extractor(soup)
        extractor.parse()
        se_it_table = extractor.return_list()
        se_it_table.pop(0)

    # Japan
    if fetch_updates:
        se_jp = requests.get('https://www.parkrun.jp/special-events',
                             headers=headers,
                             timeout=10).text
        with open('_data/special_events/jp.html',
                  'wt',
                  encoding='utf-8',
                  newline='') as f:
            f.write(se_jp)
            print(now_fn(), "_data/special_events/jp.html saved")

    with open('_data/special_events/jp.html',
              'r',
              encoding='utf-8',
              newline='\n') as f:
        soup = BeautifulSoup(f, 'html.parser')

        extractor = Extractor(soup)
        extractor.parse()
        se_jp_table = extractor.return_list()
        se_jp_table.pop(0)

    # Lithuania
    if fetch_updates:
        se_lt = requests.get('https://www.parkrun.lt/special-events',
                             headers=headers,
                             timeout=10).text
        with open('_data/special_events/lt.html',
                  'wt',
                  encoding='utf-8',
                  newline='') as f:
            f.write(se_lt)
            print(now_fn(), "_data/special_events/lt.html saved")

    with open('_data/special_events/lt.html',
              'r',
              encoding='utf-8',
              newline='\n') as f:
        soup = BeautifulSoup(f, 'html.parser')

        extractor = Extractor(soup)
        extractor.parse()
        se_lt_table = extractor.return_list()
        se_lt_table.pop(0)

    # Malaysia
    if fetch_updates:
        se_my = requests.get('https://www.parkrun.my/special-events',
                             headers=headers,
                             timeout=10).text
        with open('_data/special_events/my.html',
                  'wt',
                  encoding='utf-8',
                  newline='') as f:
            f.write(se_my)
            print(now_fn(), "_data/special_events/my.html saved")

    with open('_data/special_events/my.html',
              'r',
              encoding='utf-8',
              newline='\n') as f:
        soup = BeautifulSoup(f, 'html.parser')

        extractor = Extractor(soup)
        extractor.parse()
        se_my_table = extractor.return_list()
        se_my_table.pop(0)

    # Netherlands
    if fetch_updates:
        se_nl = requests.get('https://www.parkrun.co.nl/special-events',
                             headers=headers,
                             timeout=10).text
        with open('_data/special_events/nl.html', 'wt', encoding='utf-8', newline='') as f:
            f.write(se_nl)
            print(now_fn(), "_data/special_events/nl.html saved")

    with open('_data/special_events/nl.html', 'r', encoding='utf-8', newline='\n') as f:
        soup = BeautifulSoup(f, 'html.parser')

        extractor = Extractor(soup)
        extractor.parse()
        se_nl_table = extractor.return_list()
        se_nl_table.pop(0)

    # New Zeland
    if fetch_updates:
        se_nz = requests.get('https://www.parkrun.co.nz/special-events',
                             headers=headers,
                             timeout=10).text
        with open('_data/special_events/nz.html', 'wt', encoding='utf-8', newline='') as f:
            f.write(se_nz)
            print(now_fn(), "_data/special_events/nz.html saved")

    with open('_data/special_events/nz.html', 'r', encoding='utf-8', newline='\n') as f:
        soup = BeautifulSoup(f, 'html.parser')

        extractor = Extractor(soup)
        extractor.parse()
        se_nz_table = extractor.return_list()
        se_nz_table.pop(0)

    # Norway
    if fetch_updates:
        se_no = requests.get('https://www.parkrun.no/special-events',
                             headers=headers,
                             timeout=10).text
        with open('_data/special_events/no.html', 'wt', encoding='utf-8', newline='') as f:
            f.write(se_no)
            print(now_fn(), "_data/special_events/no.html saved")

    with open('_data/special_events/no.html', 'r', encoding='utf-8', newline='\n') as f:
        soup = BeautifulSoup(f, 'html.parser')

        extractor = Extractor(soup)
        extractor.parse()
        se_no_table = extractor.return_list()
        se_no_table.pop(0)

    # Poland
    if fetch_updates:
        se_pl = requests.get('https://www.parkrun.pl/special-events',
                             headers=headers,
                             timeout=10).text
        with open('_data/special_events/pl.html', 'wt', encoding='utf-8', newline='') as f:
            f.write(se_pl)
            print(now_fn(), "_data/special_events/pl.html saved")

    with open('_data/special_events/pl.html', 'r', encoding='utf-8', newline='\n') as f:
        soup = BeautifulSoup(f, 'html.parser')

        extractor = Extractor(soup)
        extractor.parse()
        se_pl_table = extractor.return_list()
        se_pl_table.pop(0)

    # Singapore
    if fetch_updates:
        se_sg = requests.get('https://www.parkrun.sg/special-events',
                             headers=headers,
                             timeout=10).text
        with open('_data/special_events/sg.html', 'wt', encoding='utf-8', newline='') as f:
            f.write(se_sg)
            print(now_fn(), "_data/special_events/sg.html saved")

    with open('_data/special_events/sg.html', 'r', encoding='utf-8', newline='\n') as f:
        soup = BeautifulSoup(f, 'html.parser')

        extractor = Extractor(soup)
        extractor.parse()
        se_sg_table = extractor.return_list()
        se_sg_table.pop(0)

    # South Africa
    if fetch_updates:
        se_za = requests.get('https://www.parkrun.co.za/special-events',
                             headers=headers,
                             timeout=10).text
        with open('_data/special_events/za.html', 'wt', encoding='utf-8', newline='') as f:
            f.write(se_za)
            print(now_fn(), "_data/special_events/za.html saved")

    with open('_data/special_events/za.html', 'r', encoding='utf-8', newline='\n') as f:
        soup = BeautifulSoup(f, 'html.parser')

        extractor = Extractor(soup)
        extractor.parse()
        se_za_table = extractor.return_list()
        se_za_table.pop(0)

    # Sweden
    if fetch_updates:
        se_se = requests.get('https://www.parkrun.se/special-events',
                             headers=headers,
                             timeout=10).text
        with open('_data/special_events/se.html', 'wt', encoding='utf-8', newline='') as f:
            f.write(se_se)
            print(now_fn(), "_data/special_events/se.html saved")

    with open('_data/special_events/se.html', 'r', encoding='utf-8', newline='\n') as f:
        soup = BeautifulSoup(f, 'html.parser')

        extractor = Extractor(soup)
        extractor.parse()
        se_se_table = extractor.return_list()
        se_se_table.pop(0)

    # United Kingdom
    if fetch_updates:
        se_uk = requests.get('https://www.parkrun.org.uk/special-events',
                             headers=headers,
                             timeout=10).text
        with open('_data/special_events/uk.html', 'wt', encoding='utf-8', newline='') as f:
            f.write(se_uk)
            print(now_fn(), "_data/special_events/uk.html saved")

    with open('_data/special_events/uk.html', 'r', encoding='utf-8', newline='\n') as f:
        soup = BeautifulSoup(f, 'html.parser')

        extractor = Extractor(soup)
        extractor.parse()
        se_uk_table = extractor.return_list()
        se_uk_table.pop(0)

    # United States
    if fetch_updates:
        se_us = requests.get('https://www.parkrun.us/special-events',
                             headers=headers,
                             timeout=10).text
        with open('_data/special_events/us.html', 'wt', encoding='utf-8', newline='') as f:
            f.write(se_us)
            print(now_fn(), "_data/special_events/us.html saved")

    with open('_data/special_events/us.html', 'r', encoding='utf-8', newline='\n') as f:
        soup = BeautifulSoup(f, 'html.parser')

        extractor = Extractor(soup)
        extractor.parse()
        se_us_table = extractor.return_list()
        se_us_table.pop(0)

    # Christmas Day
    se_table1 = se_au_table + se_fr_table + se_ie_table + \
        se_it_table + se_nz_table + se_uk_table
    se_table1.sort()
    for row in se_table1:
        out = {}
        out["EventLongName"] = row[0]
        if row[2] == '❌':
            out["2024-12-25"] = False
        elif row[2] == '✅':
            out["2024-12-25"] = True

        if row[3] == '❌':
            out["2025-01-01"] = False
        elif row[3] == '✅':
            out["2025-01-01"] = True

        special_events.append(out)

    # New Year's Day Only
    se_table2 = se_ca_table + se_dk_table + se_fi_table + \
        se_de_table + se_jp_table + se_my_table
    se_table2 += se_nl_table + se_no_table + se_sg_table + \
        se_za_table + se_se_table + se_lt_table
    se_table2.sort()
    for row in se_table2:
        out = {}
        out["EventLongName"] = row[0]
        if row[2] == '❌':
            out["2025-01-01"] = False
        elif row[2] == '✅':
            out["2025-01-01"] = True

        special_events.append(out)

    # Boxing Day
    se_table3 = se_pl_table
    for row in se_table3:
        out = {}
        out["EventLongName"] = row[0]
        if row[2] == '❌':
            out["2024-12-26"] = False
        elif row[2] == '✅':
            out["2024-12-26"] = True

        if row[3] == '❌':
            out["2025-01-01"] = False
        elif row[3] == '✅':
            out["2025-01-01"] = True

        special_events.append(out)

    # Thanksgiving
    se_table4 = se_us_table
    for row in se_table4:
        out = {}
        out["EventLongName"] = row[0]
        if row[2] == '❌':
            out["2024-11-28"] = False
        elif row[2] == '✅':
            out["2024-11-28"] = True

        if row[3] == '❌':
            out["2025-01-01"] = False
        elif row[3] == '✅':
            out["2025-01-01"] = True

        special_events.append(out)

    se_table = se_table1 + se_table2 + se_table3 + se_table4

    with open('_data/special_events.json', 'wt', encoding='utf-8', newline='') as f:
        f.write(json.dumps(special_events, indent=2))
        print(now_fn(), "special_events.json saved")
