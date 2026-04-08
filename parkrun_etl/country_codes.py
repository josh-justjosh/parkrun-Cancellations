"""Map parkrun countrycode (+ special cases) to website base and display country."""

NAMIBIA_EVENTS = frozenset([
    'Windhoek parkrun',
    'Omeya parkrun',
    'Swakopmund parkrun',
    'Walvis Bay parkrun',
])
ESWATINI_EVENTS = frozenset([
    'Mbabane parkrun',
    'Manzini parkrun',
])

# countrycode -> (website_base_url, Country)
COUNTRYCODE_MAP = {
    3: ('https://www.parkrun.com.au/', 'Australia'),
    4: ('https://www.parkrun.co.at/', 'Austria'),
    14: ('https://www.parkrun.ca/', 'Canada'),
    23: ('https://www.parkrun.dk/', 'Denmark'),
    30: ('https://www.parkrun.fi/', 'Finland'),
    31: ('https://www.parkrun.fr/', 'France'),
    32: ('https://www.parkrun.com.de/', 'Germany'),
    42: ('https://www.parkrun.ie/', 'Ireland'),
    44: ('https://www.parkrun.it/', 'Italy'),
    46: ('https://www.parkrun.jp/', 'Japan'),
    54: ('https://www.parkrun.lt/', 'Lithuania'),
    57: ('https://www.parkrun.my/', 'Malaysia'),
    65: ('https://www.parkrun.co.nz/', 'New Zealand'),
    67: ('https://www.parkrun.no/', 'Norway'),
    74: ('https://www.parkrun.pl/', 'Poland'),
    79: ('https://www.parkrun.ru/', 'Russia'),
    82: ('https://www.parkrun.sg/', 'Singapore'),
    88: ('https://www.parkrun.se/', 'Sweden'),
    97: ('https://www.parkrun.org.uk/', 'United Kingdom'),
    98: ('https://www.parkrun.us/', 'USA'),
    64: ('https://www.parkrun.co.nl/', 'Netherlands'),
}


def apply_country_website_and_country(properties):
    '''
    Set properties['Website'] and properties['Country'] from countrycode.
    Matches legacy elif-chain behaviour (unknown code: Website only -> Unavailable).
    '''
    cc = properties['countrycode']
    eln = properties['EventLongName']
    if cc == 85:
        properties['Website'] = 'https://www.parkrun.co.za/'
        if eln in NAMIBIA_EVENTS:
            properties['Country'] = 'Namibia'
        elif eln in ESWATINI_EVENTS:
            properties['Country'] = 'Eswatini'
        else:
            properties['Country'] = 'South Africa'
        return
    pair = COUNTRYCODE_MAP.get(cc)
    if pair:
        properties['Website'], properties['Country'] = pair
    else:
        properties['Website'] = 'Unavailable'
