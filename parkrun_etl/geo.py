import xml.etree.ElementTree as ET

import requests


def resolve_new_event_state_county(parkrun, headers, new_states_list, now_fn):
    '''
    Geonames lookup for events not in states_list.
    Mutates parkrun['properties'] State/County and appends to new_states_list.
    '''
    props = parkrun['properties']
    print(now_fn(), props['EventShortName'], 'not saved state')
    GEONAME_USERNAME = '_josh_justjosh'
    URL = "http://api.geonames.org/countrySubdivision?lat="
    URL += str(parkrun['geometry']['coordinates'][1])
    URL += "&lng=" + str(parkrun['geometry']['coordinates'][0])
    URL += "&radius=1.5&maxRows=1&level=2&username="
    URL += GEONAME_USERNAME
    root = ET.fromstring(requests.get(
        URL, headers=headers, timeout=10).text.strip())
    try:
        state = root.find('countrySubdivision').find('adminName1').text
    except BaseException:
        state = "-Unknown-"
        print(now_fn(), props['EventLongName'], "- State not Found -", URL)
    try:
        county = root.find('countrySubdivision').find('adminName2').text
    except BaseException:
        county = "-Unknown-"
        print(now_fn(), props['EventLongName'], '- County not found -', URL)
    props['State'] = state
    props['County'] = county
    add = [props['EventLongName'], props['Country'], state, county]
    new_states_list.append(add)
