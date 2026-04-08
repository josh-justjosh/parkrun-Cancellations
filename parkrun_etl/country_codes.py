"""Map parkrun countrycode (+ special cases) to website base and display country."""

from .countries_registry import (
    CODE_85_WEBSITE_BASE,
    ESWATINI_EVENTS,
    NAMIBIA_EVENTS,
    build_countrycode_map,
)

# countrycode -> (website_base_url, Country); built from countries_registry (excludes cc 85 splits).
COUNTRYCODE_MAP = build_countrycode_map()

def apply_country_website_and_country(properties):
    """
    Set properties['Website'] and properties['Country'] from countrycode.
    Matches legacy elif-chain behaviour (unknown code: Website only -> Unavailable).
    """
    cc = properties["countrycode"]
    eln = properties["EventLongName"]
    if cc == 85:
        properties["Website"] = CODE_85_WEBSITE_BASE
        if eln in NAMIBIA_EVENTS:
            properties["Country"] = "Namibia"
        elif eln in ESWATINI_EVENTS:
            properties["Country"] = "Eswatini"
        else:
            properties["Country"] = "South Africa"
        return
    pair = COUNTRYCODE_MAP.get(cc)
    if pair:
        properties["Website"], properties["Country"] = pair
    else:
        properties["Website"] = "Unavailable"
