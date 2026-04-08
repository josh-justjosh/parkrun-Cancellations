import json
import time
import csv
import collections

import requests

from .country_codes import apply_country_website_and_country
from .county_rules import normalise_uk_ie_county
from .event_features import (
    apply_map_popup_description,
    apply_special_day_flags,
)
from .geo import resolve_new_event_state_county
from .history import writehistory
from .http_headers import headers
from .outputs import (
    write_cancellation_dates_tsv,
    write_events_geojson,
    write_reasons_json,
)
from .special_events import load_special_events
from .table_utils import rem_dups, sort_by_index_0, sort_by_index_1
from .time_utils import now, same_week
from .wiki_cancellations import (
    fetch_cancellations_wiki_html,
    parse_global_cancellations_table,
)


def main():


    print(now(), 'Script Start')




    old_cancellations_data = []
    with open('_data/cancellations.tsv', 'r', encoding='utf-8', newline='') as f:
        tsv_reader = csv.reader(f, delimiter="\t")
        for row in tsv_reader:
            row = rem_dups(row)
            old_cancellations_data.append(row)
    print(now(), 'cancellations.tsv read')
    old_cancellations_data.remove(
        ['Date', 'Event', 'Country', 'Cancellation Note', 'Website'])

    states_list = []
    with open('_data/raw/states.tsv', 'r', encoding='utf-8', newline='') as f:
        tsv_reader = csv.reader(f, delimiter="\t")
        for row in tsv_reader:
            states_list.append(row)
    print(now(), 'raw/states.tsv read')
    states_list.remove(['Event', 'Country', 'State', 'County'])



    events = requests.get('https://images.parkrun.com/events.json',
                          headers=headers, timeout=10).text

    with open('_data/raw/events.json', 'wt', encoding='utf-8', newline='') as f:
        f.write(json.dumps(json.loads(events), indent=2))
        print(now(), "raw/events.json saved")

    # This data has been removed from the wiki
    '''tei = requests.get(
        'https://wiki.parkrun.com/index.php/Technical_Event_Information',
        headers=headers,
        timeout=10).text

    technical_event_info = tei

    with open('_data/raw/tei.html', 'wt', encoding='utf-8', newline='') as f:
        f.write(technical_event_info)
        print(now(), "raw/tei.html saved")
    soup = BeautifulSoup(technical_event_info, 'html.parser')

    extractor = Extractor(soup)
    extractor.parse()
    tei_table = extractor.return_list()
    # print(now(),tei_table)

    upcoming_events_table = []
    upcoming_events = []

    for i in tei_table:
        out = []
        for j in i:
            j = j.strip()
            out.append(j)
        # print(now(),out)
        if 'AcceptingRegistrations' in out:
            upcoming_events.append(out[0])
            upcoming_events_table.append(out)'''

    upcoming_events_table = []
    upcoming_events = []

    # upcoming_events.append('Central parkrun, Plymouth')
    # upcoming_events.append('Church Mead parkrun')
    # upcoming_events.append('Edgbaston Reservoir parkrun')
    # upcoming_events.append('Henlow Bridge Lakes parkrun')
    # upcoming_events.append('Penryn Campus parkrun')
    # upcoming_events.append('Roberts Park parkrun')

    print(now(), 'Upcoming Events:', upcoming_events)

    print(now(),
          'getting cancellations data (wiki API parse, else index.php scoped table)')

    cancellations, cancellations_fetch_source = fetch_cancellations_wiki_html()
    print(now(), 'cancellations HTML source:', cancellations_fetch_source)

    with open('_data/raw/cancellations.html', 'wt', encoding='utf-8', newline='') as f:
        f.write(cancellations)
        print(now(), "raw/cancellations.html saved")

    events = json.loads(events)['events']

    cancellation_table = parse_global_cancellations_table(cancellations)
    if not cancellation_table:
        print(now(), 'WARNING: no cancellation rows parsed (empty table or parse failure)')


    cancellations_data = []
    cancellations_list = []
    cancellation_reasons = []

    for i, cancellation in enumerate(cancellation_table):
        try:
            for x in range(5):
                cancellation[x] = cancellation[x].strip()
        except IndexError:
            break

        if same_week(cancellation[0]):
            # print(now(),cancellation)
            cancellations_data.append(
                [cancellation[0], cancellation[1], cancellation[3], cancellation[4]])
            cancellations_list.append(cancellation[1])
            cancellation_reasons.append(cancellation[4])


    cancellation_reasons_count = collections.Counter(cancellation_reasons)
    cancellation_reasons_json = {}

    for i, j in cancellation_reasons_count.items():
        cancellation_reasons_json[i] = j

    write_reasons_json(cancellation_reasons_json, now)




    cancellation_table.sort(key=sort_by_index_0)
    cancellation_table.sort(key=sort_by_index_1)


    with open('_data/all-cancellations.tsv',
              'wt',
              encoding='utf-8',
              newline='') as f:
        tsv_writer = csv.writer(f, delimiter='\t')
        tsv_writer.writerow(
            ['Date', 'Event', 'Region', 'Country', 'Cancellation Note'])
        for i in cancellation_table:
            tsv_writer.writerow(i)
        print(now(), "all-cancellations.tsv saved")

    cancellation_dates = []
    new_states_list = []

    X = 0

    FETCH_UPDATES = False
    special_events = load_special_events(FETCH_UPDATES, headers, now)

    upcoming_set = set(upcoming_events)
    events['features'] = [
        f for f in events['features']
        if f['properties']['EventLongName'] not in upcoming_set
    ]

    for parkrun in events['features']:
        # print(now(),parkrun['properties']['EventLongName'])
        if 'junior' in parkrun['properties']['EventLongName']:
            if parkrun['properties']['EventLongName'] in cancellations_list:
                parkrun['properties']['Status'] = 'junior Cancellation'
            else:
                parkrun['properties']['Status'] = 'junior parkrunning'
        else:
            if parkrun['properties']['EventLongName'] in cancellations_list:
                parkrun['properties']['Status'] = '5k Cancellation'
            else:
                parkrun['properties']['Status'] = 'parkrunning'

        parkrun['properties']['Cancellations'] = []
        for cancellation in cancellation_table:
            if parkrun['properties']['EventLongName'] == cancellation[1] and same_week(
                    cancellation[0]):
                newcancellation = {
                    'DateCancelled': cancellation[0],
                    'ReasonCancelled': cancellation[4]}
                parkrun['properties']['Cancellations'].append(newcancellation)
                cancellation_dates.append(cancellation[0])

        apply_country_website_and_country(parkrun['properties'])

        if parkrun['properties']['Website'] != 'Unavailable':
            parkrun['properties']['Website'] += parkrun['properties']['eventname']

        NEW = True
        for event in states_list:
            if event[0] == parkrun['properties']['EventLongName']:
                # print(now(),parkrun['properties']['EventShortName'],'already saved state')
                new_states_list.append(event)
                try:
                    parkrun['properties']['State'] = event[2]
                except IndexError:
                    parkrun['properties']['State'] = "-Unknown-"
                try:
                    parkrun['properties']['County'] = event[3]
                except IndexError:
                    parkrun['properties']['County'] = "-Unknown-"
                NEW = False

        if NEW:
            resolve_new_event_state_county(
                parkrun, headers, new_states_list, now)

        apply_map_popup_description(parkrun['properties'], now)

        X += 1
        # print(now(),x,"/",len(events['features']),'-',parkrun['properties']['EventShortName'],"processed")
        # if X == 1750:
        #   break

        apply_special_day_flags(parkrun['properties'], special_events)

    write_events_geojson(events, now)

    write_cancellation_dates_tsv(cancellation_dates, now)

    events_data = []
    for event in events['features']:
        out = []
        out.append(event['properties']['EventLongName'])
        out.append(event['geometry']['coordinates'][1])
        out.append(event['geometry']['coordinates'][0])
        out.append(event['properties']['Country'])
        out.append(event['properties']['State'])
        out.append(event['properties']['County'])
        out.append(event['properties']['Status'])
        out.append(event['properties']['Cancellations'])
        out.append(event['properties']['Website'])
        events_data.append(out)
    events_data.sort()

    with open('_data/events-table.tsv', 'wt', encoding='utf-8', newline='') as f:
        tsv_writer = csv.writer(f, delimiter='\t')
        tsv_writer.writerow(['Event',
                             'Latitude',
                             'Longitude',
                             'Country',
                             'State',
                             'County',
                             'Status',
                             'Cancellations',
                             'Website'])
        for event in events_data:
            tsv_writer.writerow(event)
    print(now(), "events-table.tsv saved")

    countries = {
        'Australia': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
        'Austria': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
        'Canada': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
        'Denmark': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
        'Eswatini': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
        'Finland': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
        'France': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
        'Germany': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
        'Ireland': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
        'Italy': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
        'Japan': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
        'Lithuania': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
        'Malaysia': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
        'Namibia': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
        'Netherlands': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
        'New Zealand': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
        'Norway': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
        'Poland': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
        'Russia': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
        'Singapore': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
        'South Africa': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
        'Sweden': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
        'United Kingdom': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
        'USA': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
        'Total': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
    }

    totals = {
        'parkrunning': 0,
        'junior parkrunning': 0,
        '5k Cancellations': 0,
        'junior Cancellations': 0,
        'Total': 0
    }


    for parkrun in events['features']:
        if parkrun['properties']['Status'] == 'parkrunning':
            countries[parkrun['properties']['Country']]['parkrunning'] += 1
            countries[parkrun['properties']['Country']]['Total'] += 1
        elif parkrun['properties']['Status'] == 'junior parkrunning':
            countries[parkrun['properties']['Country']]['junior parkrunning'] += 1
            countries[parkrun['properties']['Country']]['Total'] += 1
        elif parkrun['properties']['Status'] == '5k Cancellation':
            countries[parkrun['properties']['Country']]['5k Cancellations'] += 1
            countries[parkrun['properties']['Country']]['Total'] += 1
        elif parkrun['properties']['Status'] == 'junior Cancellation':
            countries[parkrun['properties']['Country']
                      ]['junior Cancellations'] += 1
            countries[parkrun['properties']['Country']]['Total'] += 1
        elif parkrun['properties']['Status'] == 'PtR':
            countries[parkrun['properties']['Country']]['5k Cancellations'] += 1
            countries[parkrun['properties']['Country']]['Total'] += 1
        else:
            print(now(), "Error:", parkrun['properties']['EventLongName'])
    # print(now(),countries)

    for country, data in countries.items():
        totals['parkrunning'] += data['parkrunning']
        totals['junior parkrunning'] += data['junior parkrunning']
        totals['5k Cancellations'] += data['5k Cancellations']
        totals['junior Cancellations'] += data['junior Cancellations']
        totals['Total'] += data['Total']

    countries['Total'] = totals

    with open('_data/countries-data.tsv', 'wt', encoding='utf-8', newline='') as f:
        tsv_writer = csv.writer(f, delimiter='\t')
        tsv_writer.writerow(['Country', 'parkrunning', 'junior parkrunning',
                            '5k Cancellations', 'junior Cancellations', 'Total'])
        for i, j in countries.items():
            out = [i]
            for k, l in j.items():
                if l != 0:
                    out.append(l)
                else:
                    out.append('')
            tsv_writer.writerow(out)
    print(now(), "countries-data.tsv saved")

    uk = {
        'England': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
        'Northern Ireland': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
        'Scotland': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
        'Wales': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
        'Other': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
        'Total': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
    }

    uk_totals = {
        'parkrunning': 0,
        'junior parkrunning': 0,
        '5k Cancellations': 0,
        'junior Cancellations': 0,
        'Total': 0
    }

    for parkrun in events['features']:
        if parkrun['properties']['Country'] == "United Kingdom":
            if parkrun['properties']['State'] in [
                    'England', 'Northern Ireland', 'Scotland', 'Wales']:
                if parkrun['properties']['Status'] == 'parkrunning':
                    uk[parkrun['properties']['State']]['parkrunning'] += 1
                    uk[parkrun['properties']['State']]['Total'] += 1
                elif parkrun['properties']['Status'] == 'junior parkrunning':
                    uk[parkrun['properties']['State']]['junior parkrunning'] += 1
                    uk[parkrun['properties']['State']]['Total'] += 1
                elif parkrun['properties']['Status'] == '5k Cancellation':
                    uk[parkrun['properties']['State']]['5k Cancellations'] += 1
                    uk[parkrun['properties']['State']]['Total'] += 1
                elif parkrun['properties']['Status'] == 'junior Cancellation':
                    uk[parkrun['properties']['State']]['junior Cancellations'] += 1
                    uk[parkrun['properties']['State']]['Total'] += 1
                elif parkrun['properties']['Status'] == 'PtR':
                    uk[parkrun['properties']['State']]['5k Cancellations'] += 1
                    uk[parkrun['properties']['State']]['Total'] += 1
            else:
                if parkrun['properties']['Status'] == 'parkrunning':
                    uk['Other']['parkrunning'] += 1
                    uk['Other']['Total'] += 1
                elif parkrun['properties']['Status'] == 'junior parkrunning':
                    uk['Other']['junior parkrunning'] += 1
                    uk['Other']['Total'] += 1
                elif parkrun['properties']['Status'] == '5k Cancellation':
                    uk['Other']['5k Cancellations'] += 1
                    uk['Other']['Total'] += 1
                elif parkrun['properties']['Status'] == 'junior Cancellation':
                    uk['Other']['junior Cancellations'] += 1
                    uk['Other']['Total'] += 1
                elif parkrun['properties']['Status'] == 'PtR':
                    uk['Other']['5k Cancellations'] += 1
                    uk['Other']['Total'] += 1

    # print(now(),countries)

    for state, data in uk.items():
        uk_totals['parkrunning'] += data['parkrunning']
        uk_totals['junior parkrunning'] += data['junior parkrunning']
        uk_totals['5k Cancellations'] += data['5k Cancellations']
        uk_totals['junior Cancellations'] += data['junior Cancellations']
        uk_totals['Total'] += data['Total']

    uk['Total'] = uk_totals

    with open('_data/uk-data.tsv', 'wt', encoding='utf-8', newline='') as f:
        tsv_writer = csv.writer(f, delimiter='\t')
        tsv_writer.writerow(['Country', 'parkrunning', 'junior parkrunning',
                            '5k Cancellations', 'junior Cancellations', 'Total'])
        for i, j in uk.items():
            out = [i]
            for k, l in j.items():
                if l != 0:
                    out.append(l)
                else:
                    out.append('')
            tsv_writer.writerow(out)
    print(now(), "uk-data.tsv saved")

    aus = {
        'Australian Capital Territory': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
        'New South Wales': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
        'Northern Territory': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
        'Queensland': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
        'South Australia': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
        'Tasmania': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
        'Victoria': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
        'Western Australia': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
        'Total': {
            'parkrunning': 0,
            'junior parkrunning': 0,
            '5k Cancellations': 0,
            'junior Cancellations': 0,
            'Total': 0
        },
    }

    aus_totals = {
        'parkrunning': 0,
        'junior parkrunning': 0,
        '5k Cancellations': 0,
        'junior Cancellations': 0,
        'Total': 0
    }

    for parkrun in events['features']:
        if parkrun['properties']['Country'] == "Australia":
            if parkrun['properties']['State'] in [
                'Queensland',
                'New South Wales',
                'Victoria',
                'Australian Capital Territory',
                'Western Australia',
                'Tasmania',
                'South Australia',
                    'Northern Territory']:
                if parkrun['properties']['Status'] == 'parkrunning':
                    aus[parkrun['properties']['State']]['parkrunning'] += 1
                    aus[parkrun['properties']['State']]['Total'] += 1
                elif parkrun['properties']['Status'] == 'junior parkrunning':
                    aus[parkrun['properties']['State']]['junior parkrunning'] += 1
                    aus[parkrun['properties']['State']]['Total'] += 1
                elif parkrun['properties']['Status'] == '5k Cancellation':
                    aus[parkrun['properties']['State']]['5k Cancellations'] += 1
                    aus[parkrun['properties']['State']]['Total'] += 1
                elif parkrun['properties']['Status'] == 'junior Cancellation':
                    aus[parkrun['properties']['State']]['junior Cancellations'] += 1
                    aus[parkrun['properties']['State']]['Total'] += 1
                elif parkrun['properties']['Status'] == 'PtR':
                    aus[parkrun['properties']['State']]['5k Cancellations'] += 1
                    aus[parkrun['properties']['State']]['Total'] += 1
            else:
                print(now(), parkrun['properties']['EventLongName'],
                      "in Australia but not in state")

    # print(now(),countries)

    for state, data in aus.items():
        aus_totals['parkrunning'] += data['parkrunning']
        aus_totals['junior parkrunning'] += data['junior parkrunning']
        aus_totals['5k Cancellations'] += data['5k Cancellations']
        aus_totals['junior Cancellations'] += data['junior Cancellations']
        aus_totals['Total'] += data['Total']

    aus['Total'] = aus_totals

    with open('_data/aus-data.tsv', 'wt', encoding='utf-8', newline='') as f:
        tsv_writer = csv.writer(f, delimiter='\t')
        tsv_writer.writerow(['Country', 'parkrunning', 'junior parkrunning',
                            '5k Cancellations', 'junior Cancellations', 'Total'])
        for i, j in aus.items():
            out = [i]
            for k, l in j.items():
                if l != 0:
                    out.append(l)
                else:
                    out.append('')
            tsv_writer.writerow(out)
    print(now(), "aus-data.tsv saved")

    uk_ie_counties = {}
    for parkrun in events['features']:
        if parkrun['properties']['Country'] in ["United Kingdom", "Ireland"]:
            if parkrun['properties']['County'] not in ['', 'Douglas']:
                normalise_uk_ie_county(parkrun['properties'])

                if parkrun['properties']['County'] not in uk_ie_counties:
                    if parkrun['properties']['State'] in [
                            'England', 'Northern Ireland', 'Scotland', 'Wales']:
                        uk_ie_counties[
                            parkrun['properties']['County']] = {
                            'country': parkrun['properties']['State'],
                            'parkrunning': 0,
                            'junior parkrunning': 0,
                            '5k Cancellations': 0,
                            'junior Cancellations': 0,
                            'Total': 0,
                            'events parkrunning': '',
                            'events junior parkrunning': '',
                            'events 5k cancellation': '',
                            'events junior cancellation': ''}
                    else:
                        uk_ie_counties[
                            parkrun['properties']['County']] = {
                            'country': parkrun['properties']['Country'],
                            'parkrunning': 0,
                            'junior parkrunning': 0,
                            '5k Cancellations': 0,
                            'junior Cancellations': 0,
                            'Total': 0,
                            'events parkrunning': '',
                            'events junior parkrunning': '',
                            'events 5k cancellation': '',
                            'events junior cancellation': ''}
                if parkrun['properties']['Status'] == 'parkrunning':
                    uk_ie_counties[parkrun['properties']
                                   ['County']]['parkrunning'] += 1
                    uk_ie_counties[parkrun['properties']['County']]['Total'] += 1
                    uk_ie_counties[parkrun['properties']['County']
                                   ]['events parkrunning'] += parkrun['properties']['EventShortName'] + '|'
                elif parkrun['properties']['Status'] == 'junior parkrunning':
                    uk_ie_counties[parkrun['properties']
                                   ['County']]['junior parkrunning'] += 1
                    uk_ie_counties[parkrun['properties']['County']]['Total'] += 1
                    uk_ie_counties[parkrun['properties']['County']
                                   ]['events junior parkrunning'] += parkrun['properties']['EventShortName'] + '|'
                elif parkrun['properties']['Status'] == '5k Cancellation':
                    uk_ie_counties[parkrun['properties']
                                   ['County']]['5k Cancellations'] += 1
                    uk_ie_counties[parkrun['properties']['County']]['Total'] += 1
                    uk_ie_counties[parkrun['properties']['County']
                                   ]['events 5k cancellation'] += parkrun['properties']['EventShortName'] + '|'
                elif parkrun['properties']['Status'] == 'junior Cancellation':
                    uk_ie_counties[parkrun['properties']
                                   ['County']]['junior Cancellations'] += 1
                    uk_ie_counties[parkrun['properties']['County']]['Total'] += 1
                    uk_ie_counties[parkrun['properties']['County']
                                   ]['events junior cancellation'] += parkrun['properties']['EventShortName'] + '|'

    uk_ie_counties_od = collections.OrderedDict(sorted(uk_ie_counties.items()))
    uk_ie_counties = {}
    for k, v in uk_ie_counties_od.items():
        uk_ie_counties[k] = v

    uk_ie_counties_totals = {
        'country': '',
        'parkrunning': 0,
        'junior parkrunning': 0,
        '5k Cancellations': 0,
        'junior Cancellations': 0,
        'Total': 0
    }
    england_totals = {
        'country': 'England',
        'parkrunning': 0,
        'junior parkrunning': 0,
        '5k Cancellations': 0,
        'junior Cancellations': 0,
        'Total': 0
    }
    ni_totals = {
        'country': 'Northern Ireland',
        'parkrunning': 0,
        'junior parkrunning': 0,
        '5k Cancellations': 0,
        'junior Cancellations': 0,
        'Total': 0
    }
    scotland_totals = {
        'country': 'Scotland',
        'parkrunning': 0,
        'junior parkrunning': 0,
        '5k Cancellations': 0,
        'junior Cancellations': 0,
        'Total': 0
    }
    wales_totals = {
        'country': 'Wales',
        'parkrunning': 0,
        'junior parkrunning': 0,
        '5k Cancellations': 0,
        'junior Cancellations': 0,
        'Total': 0
    }
    ireland_totals = {
        'country': 'Ireland',
        'parkrunning': 0,
        'junior parkrunning': 0,
        '5k Cancellations': 0,
        'junior Cancellations': 0,
        'Total': 0
    }

    for county, data in uk_ie_counties.items():
        uk_ie_counties_totals['parkrunning'] += data['parkrunning']
        uk_ie_counties_totals['junior parkrunning'] += data['junior parkrunning']
        uk_ie_counties_totals['5k Cancellations'] += data['5k Cancellations']
        uk_ie_counties_totals['junior Cancellations'] += data['junior Cancellations']
        uk_ie_counties_totals['Total'] += data['Total']
        if data['country'] == 'England':
            england_totals['parkrunning'] += data['parkrunning']
            england_totals['junior parkrunning'] += data['junior parkrunning']
            england_totals['5k Cancellations'] += data['5k Cancellations']
            england_totals['junior Cancellations'] += data['junior Cancellations']
            england_totals['Total'] += data['Total']
        if data['country'] == 'Northern Ireland':
            ni_totals['parkrunning'] += data['parkrunning']
            ni_totals['junior parkrunning'] += data['junior parkrunning']
            ni_totals['5k Cancellations'] += data['5k Cancellations']
            ni_totals['junior Cancellations'] += data['junior Cancellations']
            ni_totals['Total'] += data['Total']
        if data['country'] == 'Scotland':
            scotland_totals['parkrunning'] += data['parkrunning']
            scotland_totals['junior parkrunning'] += data['junior parkrunning']
            scotland_totals['5k Cancellations'] += data['5k Cancellations']
            scotland_totals['junior Cancellations'] += data['junior Cancellations']
            scotland_totals['Total'] += data['Total']
        if data['country'] == 'Wales':
            wales_totals['parkrunning'] += data['parkrunning']
            wales_totals['junior parkrunning'] += data['junior parkrunning']
            wales_totals['5k Cancellations'] += data['5k Cancellations']
            wales_totals['junior Cancellations'] += data['junior Cancellations']
            wales_totals['Total'] += data['Total']
        if data['country'] == 'Ireland':
            ireland_totals['parkrunning'] += data['parkrunning']
            ireland_totals['junior parkrunning'] += data['junior parkrunning']
            ireland_totals['5k Cancellations'] += data['5k Cancellations']
            ireland_totals['junior Cancellations'] += data['junior Cancellations']
            ireland_totals['Total'] += data['Total']

    uk_ie_counties['England Total'] = england_totals
    uk_ie_counties['NI Total'] = ni_totals
    uk_ie_counties['Scotland Total'] = scotland_totals
    uk_ie_counties['Wales Total'] = wales_totals
    uk_ie_counties['Ireland Total'] = ireland_totals
    uk_ie_counties['Total'] = uk_ie_counties_totals
    # print(json.dumps(uk_ie_counties, indent=4))

    usstateslist = [
        {'name': 'Alabama', 'code': 'al'},
        {'name': 'Alaska', 'code': 'ak'},
        {'name': 'Arizona', 'code': 'az'},
        {'name': 'Arkansas', 'code': 'ar'},
        {'name': 'California', 'code': 'ca'},
        {'name': 'Colorado', 'code': 'co'},
        {'name': 'Connecticut', 'code': 'ct'},
        {'name': 'Delaware', 'code': 'de'},
        {'name': 'Washington, D.C.', 'code': 'dc'},
        {'name': 'Florida', 'code': 'fl'},
        {'name': 'Georgia', 'code': 'ga'},
        {'name': 'Hawaii', 'code': 'hi'},
        {'name': 'Idaho', 'code': 'id'},
        {'name': 'Illinois', 'code': 'il'},
        {'name': 'Indiana', 'code': 'in'},
        {'name': 'Iowa', 'code': 'ia'},
        {'name': 'Kansas', 'code': 'ks'},
        {'name': 'Kentucky', 'code': 'ky'},
        {'name': 'Louisiana', 'code': 'la'},
        {'name': 'Maine', 'code': 'me'},
        {'name': 'Maryland', 'code': 'md'},
        {'name': 'Massachusetts', 'code': 'ma'},
        {'name': 'Michigan', 'code': 'mi'},
        {'name': 'Minnesota', 'code': 'mn'},
        {'name': 'Mississippi', 'code': 'ms'},
        {'name': 'Missouri', 'code': 'mo'},
        {'name': 'Montana', 'code': 'mt'},
        {'name': 'Nebraska', 'code': 'ne'},
        {'name': 'Nevada', 'code': 'nv'},
        {'name': 'New Hampshire', 'code': 'nh'},
        {'name': 'New Jersey', 'code': 'nj'},
        {'name': 'New Mexico', 'code': 'nm'},
        {'name': 'New York', 'code': 'ny'},
        {'name': 'North Carolina', 'code': 'nc'},
        {'name': 'North Dakota', 'code': 'nd'},
        {'name': 'Ohio', 'code': 'oh'},
        {'name': 'Oklahoma', 'code': 'ok'},
        {'name': 'Oregon', 'code': 'or'},
        {'name': 'Pennsylvania', 'code': 'pa'},
        {'name': 'Rhode Island', 'code': 'ri'},
        {'name': 'South Carolina', 'code': 'sc'},
        {'name': 'South Dakota', 'code': 'sd'},
        {'name': 'Tennessee', 'code': 'tn'},
        {'name': 'Texas', 'code': 'tx'},
        {'name': 'Utah', 'code': 'ut'},
        {'name': 'Vermont', 'code': 'vt'},
        {'name': 'Virginia', 'code': 'va'},
        {'name': 'Washington', 'code': 'wa'},
        {'name': 'West Virginia', 'code': 'wv'},
        {'name': 'Wisconsin', 'code': 'wi'},
        {'name': 'Wyoming', 'code': 'wy'}
    ]

    usa_states = {}

    for i in usstateslist:
        usa_states[i['name']] = {'country': 'USA',
                                 'parkrunning': 0,
                                 'junior parkrunning': 0,
                                 '5k Cancellations': 0,
                                 'junior Cancellations': 0,
                                 'Total': 0,
                                 'events parkrunning': '',
                                 'events junior parkrunning': '',
                                 'events 5k cancellation': '',
                                 'events junior cancellation': ''}

    for parkrun in events['features']:
        if parkrun['properties']['Country'] in ["USA"]:
            if parkrun['properties']['State'] not in usa_states.keys():
                usa_states[parkrun['properties']['State']] = {'parkrunning': 0,
                                                              'junior parkrunning': 0,
                                                              '5k Cancellations': 0,
                                                              'junior Cancellations': 0,
                                                              'Total': 0,
                                                              'events parkrunning': '',
                                                              'events junior parkrunning': '',
                                                              'events 5k cancellation': '',
                                                              'events junior cancellation': ''}
            if parkrun['properties']['Status'] == 'parkrunning':
                usa_states[parkrun['properties']['State']]['parkrunning'] += 1
                usa_states[parkrun['properties']['State']]['Total'] += 1
                usa_states[parkrun['properties']['State']
                           ]['events parkrunning'] += parkrun['properties']['EventShortName'] + '|'
            elif parkrun['properties']['Status'] == 'junior parkrunning':
                usa_states[parkrun['properties']
                           ['State']]['junior parkrunning'] += 1
                usa_states[parkrun['properties']['State']]['Total'] += 1
                usa_states[parkrun['properties']['State']
                           ]['events junior parkrunning'] += parkrun['properties']['EventShortName'] + '|'
            elif parkrun['properties']['Status'] == '5k Cancellation':
                usa_states[parkrun['properties']['State']]['5k Cancellations'] += 1
                usa_states[parkrun['properties']['State']]['Total'] += 1
                usa_states[parkrun['properties']['State']
                           ]['events 5k cancellation'] += parkrun['properties']['EventShortName'] + '|'
            elif parkrun['properties']['Status'] == 'junior Cancellation':
                usa_states[parkrun['properties']['State']
                           ]['junior Cancellations'] += 1
                usa_states[parkrun['properties']['State']]['Total'] += 1
                usa_states[parkrun['properties']['State']
                           ]['events junior cancellation'] += parkrun['properties']['EventShortName'] + '|'

    usa_states_od = collections.OrderedDict(sorted(usa_states.items()))
    usa_states = {}
    for k, v in usa_states_od.items():
        usa_states[k] = v

    usa_states['USA Total'] = countries['USA']
    usa_states['USA Total']['country'] = 'USA'

    with open('_data/counties/england.tsv', 'wt', encoding='utf-8', newline='') as f:
        tsv_writer = csv.writer(f, delimiter='\t')
        tsv_writer.writerow(['County',
                             'parkrunning',
                             'junior parkrunning',
                             '5k Cancellations',
                             'junior Cancellations',
                             'Total',
                             '5k Events Running',
                             'junior Events Running',
                             '5k Events Cancelled',
                             'junior Events Cancelled'])
        for i, j in uk_ie_counties.items():
            if j['country'] == 'England':
                if i == 'England Total':
                    out = ['Total']
                else:
                    out = [i]
                for k, l in j.items():
                    if l == 'England':
                        pass
                    elif l not in [0, []]:
                        out.append(l)
                    else:
                        out.append('')
                if i == 'England Total':
                    for x in range(4):
                        out.append('')
                tsv_writer.writerow(out)
    print(now(), "counties/england.tsv saved")

    with open('_data/counties/ni.tsv', 'wt', encoding='utf-8', newline='') as f:
        tsv_writer = csv.writer(f, delimiter='\t')
        tsv_writer.writerow(['County',
                             'parkrunning',
                             'junior parkrunning',
                             '5k Cancellations',
                             'junior Cancellations',
                             'Total',
                             '5k Events Running',
                             'junior Events Running',
                             '5k Events Cancelled',
                             'junior Events Cancelled'])
        for i, j in uk_ie_counties.items():
            if j['country'] == 'Northern Ireland':
                if i == 'NI Total':
                    out = ['Total']
                else:
                    out = [i]
                for k, l in j.items():
                    if l == 'Northern Ireland':
                        pass
                    elif l not in [0, []]:
                        out.append(l)
                    else:
                        out.append('')
                if i == 'NI Total':
                    for x in range(4):
                        out.append('')
                tsv_writer.writerow(out)
    print(now(), "counties/ni.tsv saved")

    with open('_data/counties/scotland.tsv', 'wt', encoding='utf-8', newline='') as f:
        tsv_writer = csv.writer(f, delimiter='\t')
        tsv_writer.writerow(['County',
                             'parkrunning',
                             'junior parkrunning',
                             '5k Cancellations',
                             'junior Cancellations',
                             'Total',
                             '5k Events Running',
                             'junior Events Running',
                             '5k Events Cancelled',
                             'junior Events Cancelled'])
        for i, j in uk_ie_counties.items():
            if j['country'] == 'Scotland':
                if i == 'Scotland Total':
                    out = ['Total']
                else:
                    out = [i]
                for k, l in j.items():
                    if l == 'Scotland':
                        pass
                    elif l not in [0, []]:
                        out.append(l)
                    else:
                        out.append('')
                if i == 'Scotland Total':
                    for x in range(4):
                        out.append('')
                tsv_writer.writerow(out)
    print(now(), "counties/scotalnd.tsv saved")

    with open('_data/counties/wales.tsv', 'wt', encoding='utf-8', newline='') as f:
        tsv_writer = csv.writer(f, delimiter='\t')
        tsv_writer.writerow(['County',
                             'parkrunning',
                             'junior parkrunning',
                             '5k Cancellations',
                             'junior Cancellations',
                             'Total',
                             '5k Events Running',
                             'junior Events Running',
                             '5k Events Cancelled',
                             'junior Events Cancelled'])
        for i, j in uk_ie_counties.items():
            if j['country'] == 'Wales':
                if i == 'Wales Total':
                    out = ['Total']
                else:
                    out = [i]
                for k, l in j.items():
                    if l == 'Wales':
                        pass
                    elif l not in [0, []]:
                        out.append(l)
                    else:
                        out.append('')
                if i == 'Wales Total':
                    for x in range(4):
                        out.append('')
                tsv_writer.writerow(out)
    print(now(), "counties/wales.tsv saved")

    with open('_data/counties/ireland.tsv', 'wt', encoding='utf-8', newline='') as f:
        tsv_writer = csv.writer(f, delimiter='\t')
        tsv_writer.writerow(['County',
                             'parkrunning',
                             'junior parkrunning',
                             '5k Cancellations',
                             'junior Cancellations',
                             'Total',
                             '5k Events Running',
                             'junior Events Running',
                             '5k Events Cancelled',
                             'junior Events Cancelled'])
        for i, j in uk_ie_counties.items():
            if j['country'] == 'Ireland':
                if i == 'Ireland Total':
                    out = ['Total']
                else:
                    out = [i]
                for k, l in j.items():
                    if l == 'Ireland':
                        pass
                    elif l not in [0, []]:
                        out.append(l)
                    else:
                        out.append('')
                if i == 'Ireland Total':
                    for x in range(4):
                        out.append('')
                tsv_writer.writerow(out)
    print(now(), "counties/ireland.tsv saved")

    with open('_data/counties/all.tsv', 'wt', encoding='utf-8', newline='') as f:
        tsv_writer = csv.writer(f, delimiter='\t')
        tsv_writer.writerow(['County',
                             'Country',
                             'parkrunning',
                             'junior parkrunning',
                             '5k Cancellations',
                             'junior Cancellations',
                             'Total',
                             '5k Events Running',
                             'junior Events Running',
                             '5k Events Cancelled',
                             'junior Events Cancelled'])
        for i, j in uk_ie_counties.items():
            out = [i]
            for k, l in j.items():
                if l not in [0, []]:
                    out.append(l)
                else:
                    out.append('')
            if 'Total' in i:
                for x in range(4):
                    out.append('')
            tsv_writer.writerow(out)
    print(now(), "counties/all.tsv saved")

    with open('_data/usa-states.tsv', 'wt', encoding='utf-8', newline='') as f:
        tsv_writer = csv.writer(f, delimiter='\t')
        tsv_writer.writerow(['States',
                             'parkrunning',
                             'junior parkrunning',
                             '5k Cancellations',
                             'junior Cancellations',
                             'Total',
                             '5k Events Running',
                             'junior Events Running',
                             '5k Events Cancelled',
                             'junior Events Cancelled'])
        for i, j in usa_states.items():
            if j['country'] == 'USA':
                if i == 'USA Total':
                    out = ['USA']
                else:
                    out = [i]
                for k, l in j.items():
                    if l == 'USA':
                        pass
                    elif l not in [0, []]:
                        out.append(l)
                    else:
                        out.append('')
                if i == 'USA Total':
                    for x in range(4):
                        out.append('')
                tsv_writer.writerow(out)
    print(now(), "usa-states.tsv saved")

    cancellations_changes = []
    cancellations_additions = []
    cancellations_removals = []

    for i in old_cancellations_data:
        try:
            oldwebsite = i[4]
            i.pop(4)
        except IndexError:
            oldwebsite = None
        if i not in cancellations_data:
            # i.append('Removed')
            out = i
            for parkrun in events['features']:
                if parkrun['properties']['EventLongName'] == i[1]:
                    out.append(oldwebsite)
                    break
            cancellations_removals.append(out)

    for i in cancellations_data:
        if i not in old_cancellations_data:
            # i.append('Added')
            out = i
            for parkrun in events['features']:
                if parkrun['properties']['EventLongName'] == i[1]:
                    out.append(parkrun['properties']['Website'])
                    break
            cancellations_additions.append(out)

    for cancellation in cancellations_data:
        if len(cancellation) <= 4:
            out = ''
            for parkrun in events['features']:
                if parkrun['properties']['EventLongName'] == cancellation[1]:
                    out = parkrun['properties']['Website']
                    break
            cancellation.append(out)
            cancellation = rem_dups(cancellation)
            # print(now(),cancellation)

    # print(now(),cancellations_changes)
    cancellations_additions.sort()
    cancellations_removals.sort()
    cancellations_data.sort(key=sort_by_index_0)
    cancellations_data.sort(key=sort_by_index_1)

    with open('_data/cancellations.tsv', 'wt', encoding='utf-8', newline='') as f:
        tsv_writer = csv.writer(f, delimiter='\t')
        tsv_writer.writerow(['Date', 'Event', 'Country',
                            'Cancellation Note', 'Website'])
        for event in cancellations_data:
            tsv_writer.writerow(event)
    print(now(), "cancellations.tsv saved")

    if cancellations_additions != []:
        with open('_data/cancellation-additions.tsv', 'wt', encoding='utf-8', newline='') as f:
            tsv_writer = csv.writer(f, delimiter='\t')
            tsv_writer.writerow(['Date', 'Event', 'Country',
                                'Cancellation Note', 'Website'])
            for event in cancellations_additions:
                tsv_writer.writerow(event)
                event.append('Added')
                cancellations_changes.append(event)
            tsv_writer.writerow([now(), '', '', ''])
        print(now(), "cancellation-additions.tsv saved")


    if cancellations_removals != []:
        with open('_data/cancellation-removals.tsv', 'wt', encoding='utf-8', newline='') as f:
            tsv_writer = csv.writer(f, delimiter='\t')
            tsv_writer.writerow(['Date', 'Event', 'Country',
                                'Previous Cancellation Note', 'Website'])
            for event in cancellations_removals:
                tsv_writer.writerow(event)
                event.append('Removed')
                cancellations_changes.append(event)
            tsv_writer.writerow([now(), '', '', ''])
        print(now(), "cancellation-removals.tsv saved")

    cancellations_changes.sort()

    if cancellations_changes != []:
        with open('_data/cancellation-changes.tsv', 'wt', encoding='utf-8', newline='') as f:
            tsv_writer = csv.writer(f, delimiter='\t')
            tsv_writer.writerow(['Date',
                                 'Event',
                                 'Country',
                                 'Cancellation Note',
                                 'Website',
                                 'Added or Removed'])
            for event in cancellations_changes:
                tsv_writer.writerow(event)
            tsv_writer.writerow([now(), '', '', '', ''])
        print(now(), "cancellation-changes.tsv saved")

        now_saved = now()

        if now_saved.month < 10:
            month = '0' + str(now_saved.month)
        else:
            month = str(now_saved.month)

        if now_saved.day < 10:
            day = '0' + str(now_saved.day)
        else:
            day = str(now_saved.day)

        if now_saved.hour < 10:
            hour = '0' + str(now_saved.hour)
        else:
            hour = str(now_saved.hour)

        if now_saved.minute < 10:
            minute = '0' + str(now_saved.minute)
        else:
            minute = str(now_saved.minute)

        if now_saved.second < 10:
            second = '0' + str(now_saved.second)
        else:
            second = str(now_saved.second)

        file = str(now_saved.year) + '-' + month + '-' + day + \
            '-' + hour + minute + second + '-update.md'

        with open('_posts/Cancellation Updates/' + file, "w+", encoding='utf-8', newline='') as f:
            out = '---' + '\n'
            out += 'layout: post' + '\n'
            out += 'title: ' + str(now_saved.year) + '/' + month + '/' + \
                day + ' ' + hour + ':' + minute + ' UTC Update' + '\n'
            out += 'date: ' + str(now_saved.year) + '-' + month + '-' + \
                day + ' ' + hour + ':' + minute + ':' + second + ' +0000' + '\n'
            out += 'author: Cancellations Bot' + '\n'
            out += "category: 'Cancellation Update'" + '\n\n'
            out += '---' + '\n'
            out += '\n'
            if cancellations_additions != []:
                out += '<h3>New Cancellations</h3>' + '\n'
                out += "<div class='hscrollable'>" + '\n'
                out += "<table style='width: 100%'>" + '\n'
                out += '    <tr>' + '\n'
                out += '        <th>Event</th>' + '\n'
                out += '        <th>Country</th>' + '\n'
                out += '        <th>Date</th>' + '\n'
                out += '        <th>Cancellation Note</th>' + '\n'
                out += '    </tr>' + '\n'
                for event in cancellations_additions:
                    out += '    <tr>' + '\n'
                    if event[4] not in ['', 'Added']:
                        out += '        <td><a href="' + \
                            event[4] + '">' + event[1] + '</a></td>' + '\n'
                    else:
                        out += '        <td>' + event[1] + '</td>' + '\n'
                    out += '        <td>' + event[2] + '</td>' + '\n'
                    out += '        <td>' + event[0] + '</td>' + '\n'
                    out += '        <td>' + event[3] + '</td>' + '\n'
                    out += '    </tr>' + '\n'
                out += '</table>' + '\n'
                out += '</div>' + '\n'
            if cancellations_removals != []:
                out += '<h3>Cancellations Removed</h3>' + '\n'
                out += "<div class='hscrollable'>" + '\n'
                out += "<table style='width: 100%'>" + '\n'
                out += '    <tr>' + '\n'
                out += '        <th>Event</th>' + '\n'
                out += '        <th>Country</th>' + '\n'
                out += '        <th>Date</th>' + '\n'
                out += '        <th>Previous Cancellation Note</th>' + '\n'
                out += '    </tr>' + '\n'
                for event in cancellations_removals:
                    out += '    <tr>' + '\n'
                    if event[4] not in ['', 'Removed']:
                        out += '        <td><a href="' + \
                            event[4] + '">' + event[1] + '</a></td>' + '\n'
                    else:
                        out += '        <td>' + event[1] + '</td>' + '\n'
                    out += '        <td>' + event[2] + '</td>' + '\n'
                    out += '        <td>' + event[0] + '</td>' + '\n'
                    out += '        <td>' + event[3] + '</td>' + '\n'
                    out += '    </tr>' + '\n'
                out += '</table>' + '\n'
                out += '</div>' + '\n'

            f.write(out)
        print(now(), file, 'saved')

    with open('_data/raw/states.tsv', 'wt', encoding='utf-8', newline='') as f:
        tsv_writer = csv.writer(f, delimiter='\t')
        tsv_writer.writerow(['Event', 'Country', 'State', 'County'])
        for event in new_states_list:
            tsv_writer.writerow(event)
    print(now(), 'raw/states.tsv saved')

    upcoming_events_table.sort()
    with open('_data/raw/ue.tsv', 'wt', encoding='utf-8', newline='') as f:
        tsv_writer = csv.writer(f, delimiter='\t')
        tsv_writer.writerow(['Event', 'Country'])
        for event in upcoming_events_table:
            tsv_writer.writerow([event[0], event[4]])
    print(now(), 'raw/ue.tsv saved')




    writehistory('global.json', countries['Total'])
    writehistory('australia.json', countries['Australia'])
    writehistory('austria.json', countries['Austria'])
    writehistory('canada.json', countries['Canada'])
    writehistory('denmark.json', countries['Denmark'])
    writehistory('eswatini.json', countries['Eswatini'])
    writehistory('finland.json', countries['Finland'])
    writehistory('france.json', countries['France'])
    writehistory('germany.json', countries['Germany'])
    writehistory('ireland.json', countries['Ireland'])
    writehistory('italy.json', countries['Italy'])
    writehistory('japan.json', countries['Japan'])
    writehistory('lithuania.json', countries['Lithuania'])
    writehistory('malaysia.json', countries['Malaysia'])
    writehistory('namibia.json', countries['Namibia'])
    writehistory('netherlands.json', countries['Netherlands'])
    writehistory('newzealand.json', countries['New Zealand'])
    writehistory('norway.json', countries['Norway'])
    writehistory('poland.json', countries['Poland'])
    writehistory('russia.json', countries['Russia'])
    writehistory('singapore.json', countries['Singapore'])
    writehistory('southafrica.json', countries['South Africa'])
    writehistory('sweden.json', countries['Sweden'])
    writehistory('unitedkingdom.json', countries['United Kingdom'])
    writehistory('unitedstates.json', countries['USA'])
    writehistory('uk/england.json', uk['England'])
    writehistory('uk/ni.json', uk['Northern Ireland'])
    writehistory('uk/scotland.json', uk['Scotland'])
    writehistory('uk/wales.json', uk['Wales'])
    writehistory('aus/act.json', aus['Australian Capital Territory'])
    writehistory('aus/nsw.json', aus['New South Wales'])
    writehistory('aus/nt.json', aus['Northern Territory'])
    writehistory('aus/qld.json', aus['Queensland'])
    writehistory('aus/sa.json', aus['South Australia'])
    writehistory('aus/tas.json', aus['Tasmania'])
    writehistory('aus/vic.json', aus['Victoria'])
    writehistory('aus/wa.json', aus['Western Australia'])

    for state in usstateslist:
        writehistory('usa/' + state['code'] + '.json', usa_states[state['name']])

    # se_au = requests.get('https://www.parkrun.com.au/special-events').text
    # se_ca = requests.get('https://www.parkrun.ca/special-events').text
    # se_dk = requests.get('https://www.parkrun.dk/special-events').text
    # se_fi = requests.get('https://www.parkrun.fi/special-events').text
    # se_fr = requests.get('https://www.parkrun.fr/special-events').text
    # se_de = requests.get('https://www.parkrun.com.de/special-events').text
    # se_ie = requests.get('https://www.parkrun.ie/special-events').text
    # se_it = requests.get('https://www.parkrun.it/special-events').text
    # se_jp = requests.get('https://www.parkrun.jp/special-events').text
    # se_lt = requests.get('https://www.parkrun.lt/special-events').text
    # se_my = requests.get('https://www.parkrun.my/special-events').text
    # se_nl = requests.get('https://www.parkrun.co.nl/special-events').text
    # se_nz = requests.get('https://www.parkrun.co.nz/special-events').text
    # se_no = requests.get('https://www.parkrun.no/special-events').text
    # se_pl = requests.get('https://www.parkrun.pl/special-events').text
    # se_sg = requests.get('https://www.parkrun.sg/special-events').text
    # se_za = requests.get('https://www.parkrun.co.za/special-events').text
    # se_se = requests.get('https://www.parkrun.se/special-events').text
    # se_uk = requests.get('https://www.parkrun.org.uk/special-events').text
    # se_us = requests.get('https://www.parkrun.us/special-events').text

    print(now(), 'Script End')

