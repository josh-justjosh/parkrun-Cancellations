"""Pure aggregation helpers for event feature GeoJSON (status counters by region)."""

import collections

from .countries_registry import iter_display_names
from .county_rules import normalise_uk_ie_county

# Status strings as emitted by the ETL (must match wiki / feature logic).
STATUS_PARKRUNNING = "parkrunning"
STATUS_JUNIOR_PARKRUNNING = "junior parkrunning"
STATUS_5K_CANCELLATION = "5k Cancellation"
STATUS_JUNIOR_CANCELLATION = "junior Cancellation"
STATUS_PTR = "PtR"

COUNTER_KEYS = (
    "parkrunning",
    "junior parkrunning",
    "5k Cancellations",
    "junior Cancellations",
    "Total",
)


def empty_region_counters():
    return {k: 0 for k in COUNTER_KEYS}


def build_countries_shell():
    countries = {n: empty_region_counters() for n in iter_display_names()}
    countries["Total"] = empty_region_counters()
    return countries


def _inc_country(countries, country_name, status):
    c = countries[country_name]
    if status == STATUS_PARKRUNNING:
        c["parkrunning"] += 1
        c["Total"] += 1
    elif status == STATUS_JUNIOR_PARKRUNNING:
        c["junior parkrunning"] += 1
        c["Total"] += 1
    elif status == STATUS_5K_CANCELLATION:
        c["5k Cancellations"] += 1
        c["Total"] += 1
    elif status == STATUS_JUNIOR_CANCELLATION:
        c["junior Cancellations"] += 1
        c["Total"] += 1
    elif status == STATUS_PTR:
        c["5k Cancellations"] += 1
        c["Total"] += 1
    else:
        return False
    return True


def aggregate_by_country(features, on_unknown_status=None):
    countries = build_countries_shell()
    for parkrun in features:
        props = parkrun["properties"]
        if not _inc_country(countries, props["Country"], props["Status"]):
            if on_unknown_status is not None:
                on_unknown_status(props.get("EventLongName", ""))
    totals = {k: 0 for k in COUNTER_KEYS}
    for _name, data in countries.items():
        for k in COUNTER_KEYS:
            totals[k] += data[k]
    countries["Total"] = totals
    return countries


def build_uk_shell():
    uk = {
        "England": empty_region_counters(),
        "Northern Ireland": empty_region_counters(),
        "Scotland": empty_region_counters(),
        "Wales": empty_region_counters(),
        "Other": empty_region_counters(),
        "Total": empty_region_counters(),
    }
    return uk


def aggregate_uk_by_nation(features):
    uk = build_uk_shell()
    uk_nations = {"England", "Northern Ireland", "Scotland", "Wales"}
    for parkrun in features:
        props = parkrun["properties"]
        if props["Country"] != "United Kingdom":
            continue
        state = props["State"]
        if state in uk_nations:
            target = uk[state]
        else:
            target = uk["Other"]
        st = props["Status"]
        if st == STATUS_PARKRUNNING:
            target["parkrunning"] += 1
            target["Total"] += 1
        elif st == STATUS_JUNIOR_PARKRUNNING:
            target["junior parkrunning"] += 1
            target["Total"] += 1
        elif st == STATUS_5K_CANCELLATION:
            target["5k Cancellations"] += 1
            target["Total"] += 1
        elif st == STATUS_JUNIOR_CANCELLATION:
            target["junior Cancellations"] += 1
            target["Total"] += 1
        elif st == STATUS_PTR:
            target["5k Cancellations"] += 1
            target["Total"] += 1
    uk_totals = {k: 0 for k in COUNTER_KEYS}
    for _state, data in uk.items():
        for k in COUNTER_KEYS:
            uk_totals[k] += data[k]
    uk["Total"] = uk_totals
    return uk


def build_aus_shell():
    states = (
        "Australian Capital Territory",
        "New South Wales",
        "Northern Territory",
        "Queensland",
        "South Australia",
        "Tasmania",
        "Victoria",
        "Western Australia",
    )
    aus = {s: empty_region_counters() for s in states}
    aus["Total"] = empty_region_counters()
    return aus


KNOWN_AUS_STATES = frozenset(
    {
        "Queensland",
        "New South Wales",
        "Victoria",
        "Australian Capital Territory",
        "Western Australia",
        "Tasmania",
        "South Australia",
        "Northern Territory",
    }
)


def aggregate_aus_by_state(features, log_fn=None):
    aus = build_aus_shell()
    for parkrun in features:
        props = parkrun["properties"]
        if props["Country"] != "Australia":
            continue
        st_name = props["State"]
        if st_name in KNOWN_AUS_STATES:
            target = aus[st_name]
            st = props["Status"]
            if st == STATUS_PARKRUNNING:
                target["parkrunning"] += 1
                target["Total"] += 1
            elif st == STATUS_JUNIOR_PARKRUNNING:
                target["junior parkrunning"] += 1
                target["Total"] += 1
            elif st == STATUS_5K_CANCELLATION:
                target["5k Cancellations"] += 1
                target["Total"] += 1
            elif st == STATUS_JUNIOR_CANCELLATION:
                target["junior Cancellations"] += 1
                target["Total"] += 1
            elif st == STATUS_PTR:
                target["5k Cancellations"] += 1
                target["Total"] += 1
        elif log_fn is not None:
            log_fn(
                props.get("EventLongName", ""),
                "in Australia but not in state",
            )
    aus_totals = {k: 0 for k in COUNTER_KEYS}
    for _state, data in aus.items():
        for k in COUNTER_KEYS:
            aus_totals[k] += data[k]
    aus["Total"] = aus_totals
    return aus


def _empty_uk_ie_county_row(country_label):
    return {
        "country": country_label,
        "parkrunning": 0,
        "junior parkrunning": 0,
        "5k Cancellations": 0,
        "junior Cancellations": 0,
        "Total": 0,
        "events parkrunning": "",
        "events junior parkrunning": "",
        "events 5k cancellation": "",
        "events junior cancellation": "",
    }


def aggregate_uk_ie_counties(features):
    uk_ie_counties = {}
    for parkrun in features:
        props = parkrun["properties"]
        if props["Country"] not in ("United Kingdom", "Ireland"):
            continue
        if props["County"] in ("", "Douglas"):
            continue
        normalise_uk_ie_county(props)
        county = props["County"]
        if county not in uk_ie_counties:
            if props["State"] in (
                "England",
                "Northern Ireland",
                "Scotland",
                "Wales",
            ):
                uk_ie_counties[county] = _empty_uk_ie_county_row(props["State"])
            else:
                uk_ie_counties[county] = _empty_uk_ie_county_row(props["Country"])
        row = uk_ie_counties[county]
        st = props["Status"]
        short = props["EventShortName"] + "|"
        if st == STATUS_PARKRUNNING:
            row["parkrunning"] += 1
            row["Total"] += 1
            row["events parkrunning"] += short
        elif st == STATUS_JUNIOR_PARKRUNNING:
            row["junior parkrunning"] += 1
            row["Total"] += 1
            row["events junior parkrunning"] += short
        elif st == STATUS_5K_CANCELLATION:
            row["5k Cancellations"] += 1
            row["Total"] += 1
            row["events 5k cancellation"] += short
        elif st == STATUS_JUNIOR_CANCELLATION:
            row["junior Cancellations"] += 1
            row["Total"] += 1
            row["events junior cancellation"] += short

    uk_ie_counties_od = collections.OrderedDict(sorted(uk_ie_counties.items()))
    uk_ie_counties = {k: v for k, v in uk_ie_counties_od.items()}

    uk_ie_counties_totals = {
        "country": "",
        "parkrunning": 0,
        "junior parkrunning": 0,
        "5k Cancellations": 0,
        "junior Cancellations": 0,
        "Total": 0,
    }
    england_totals = {
        "country": "England",
        "parkrunning": 0,
        "junior parkrunning": 0,
        "5k Cancellations": 0,
        "junior Cancellations": 0,
        "Total": 0,
    }
    ni_totals = {
        "country": "Northern Ireland",
        "parkrunning": 0,
        "junior parkrunning": 0,
        "5k Cancellations": 0,
        "junior Cancellations": 0,
        "Total": 0,
    }
    scotland_totals = {
        "country": "Scotland",
        "parkrunning": 0,
        "junior parkrunning": 0,
        "5k Cancellations": 0,
        "junior Cancellations": 0,
        "Total": 0,
    }
    wales_totals = {
        "country": "Wales",
        "parkrunning": 0,
        "junior parkrunning": 0,
        "5k Cancellations": 0,
        "junior Cancellations": 0,
        "Total": 0,
    }
    ireland_totals = {
        "country": "Ireland",
        "parkrunning": 0,
        "junior parkrunning": 0,
        "5k Cancellations": 0,
        "junior Cancellations": 0,
        "Total": 0,
    }

    for _county, data in uk_ie_counties.items():
        uk_ie_counties_totals["parkrunning"] += data["parkrunning"]
        uk_ie_counties_totals["junior parkrunning"] += data["junior parkrunning"]
        uk_ie_counties_totals["5k Cancellations"] += data["5k Cancellations"]
        uk_ie_counties_totals["junior Cancellations"] += data["junior Cancellations"]
        uk_ie_counties_totals["Total"] += data["Total"]
        if data["country"] == "England":
            for k in (
                "parkrunning",
                "junior parkrunning",
                "5k Cancellations",
                "junior Cancellations",
                "Total",
            ):
                england_totals[k] += data[k]
        if data["country"] == "Northern Ireland":
            for k in (
                "parkrunning",
                "junior parkrunning",
                "5k Cancellations",
                "junior Cancellations",
                "Total",
            ):
                ni_totals[k] += data[k]
        if data["country"] == "Scotland":
            for k in (
                "parkrunning",
                "junior parkrunning",
                "5k Cancellations",
                "junior Cancellations",
                "Total",
            ):
                scotland_totals[k] += data[k]
        if data["country"] == "Wales":
            for k in (
                "parkrunning",
                "junior parkrunning",
                "5k Cancellations",
                "junior Cancellations",
                "Total",
            ):
                wales_totals[k] += data[k]
        if data["country"] == "Ireland":
            for k in (
                "parkrunning",
                "junior parkrunning",
                "5k Cancellations",
                "junior Cancellations",
                "Total",
            ):
                ireland_totals[k] += data[k]

    uk_ie_counties["England Total"] = england_totals
    uk_ie_counties["NI Total"] = ni_totals
    uk_ie_counties["Scotland Total"] = scotland_totals
    uk_ie_counties["Wales Total"] = wales_totals
    uk_ie_counties["Ireland Total"] = ireland_totals
    uk_ie_counties["Total"] = uk_ie_counties_totals
    return uk_ie_counties


US_STATES_LIST = [
    {"name": "Alabama", "code": "al"},
    {"name": "Alaska", "code": "ak"},
    {"name": "Arizona", "code": "az"},
    {"name": "Arkansas", "code": "ar"},
    {"name": "California", "code": "ca"},
    {"name": "Colorado", "code": "co"},
    {"name": "Connecticut", "code": "ct"},
    {"name": "Delaware", "code": "de"},
    {"name": "Washington, D.C.", "code": "dc"},
    {"name": "Florida", "code": "fl"},
    {"name": "Georgia", "code": "ga"},
    {"name": "Hawaii", "code": "hi"},
    {"name": "Idaho", "code": "id"},
    {"name": "Illinois", "code": "il"},
    {"name": "Indiana", "code": "in"},
    {"name": "Iowa", "code": "ia"},
    {"name": "Kansas", "code": "ks"},
    {"name": "Kentucky", "code": "ky"},
    {"name": "Louisiana", "code": "la"},
    {"name": "Maine", "code": "me"},
    {"name": "Maryland", "code": "md"},
    {"name": "Massachusetts", "code": "ma"},
    {"name": "Michigan", "code": "mi"},
    {"name": "Minnesota", "code": "mn"},
    {"name": "Mississippi", "code": "ms"},
    {"name": "Missouri", "code": "mo"},
    {"name": "Montana", "code": "mt"},
    {"name": "Nebraska", "code": "ne"},
    {"name": "Nevada", "code": "nv"},
    {"name": "New Hampshire", "code": "nh"},
    {"name": "New Jersey", "code": "nj"},
    {"name": "New Mexico", "code": "nm"},
    {"name": "New York", "code": "ny"},
    {"name": "North Carolina", "code": "nc"},
    {"name": "North Dakota", "code": "nd"},
    {"name": "Ohio", "code": "oh"},
    {"name": "Oklahoma", "code": "ok"},
    {"name": "Oregon", "code": "or"},
    {"name": "Pennsylvania", "code": "pa"},
    {"name": "Rhode Island", "code": "ri"},
    {"name": "South Carolina", "code": "sc"},
    {"name": "South Dakota", "code": "sd"},
    {"name": "Tennessee", "code": "tn"},
    {"name": "Texas", "code": "tx"},
    {"name": "Utah", "code": "ut"},
    {"name": "Vermont", "code": "vt"},
    {"name": "Virginia", "code": "va"},
    {"name": "Washington", "code": "wa"},
    {"name": "West Virginia", "code": "wv"},
    {"name": "Wisconsin", "code": "wi"},
    {"name": "Wyoming", "code": "wy"},
]


def _empty_usa_state_row():
    return {
        "country": "USA",
        "parkrunning": 0,
        "junior parkrunning": 0,
        "5k Cancellations": 0,
        "junior Cancellations": 0,
        "Total": 0,
        "events parkrunning": "",
        "events junior parkrunning": "",
        "events 5k cancellation": "",
        "events junior cancellation": "",
    }


def _empty_usa_dynamic_row():
    return {
        "parkrunning": 0,
        "junior parkrunning": 0,
        "5k Cancellations": 0,
        "junior Cancellations": 0,
        "Total": 0,
        "events parkrunning": "",
        "events junior parkrunning": "",
        "events 5k cancellation": "",
        "events junior cancellation": "",
    }


def aggregate_usa_by_state(features, countries):
    usa_states = {}
    for i in US_STATES_LIST:
        usa_states[i["name"]] = _empty_usa_state_row()

    for parkrun in features:
        props = parkrun["properties"]
        if props["Country"] != "USA":
            continue
        state_name = props["State"]
        if state_name not in usa_states:
            usa_states[state_name] = _empty_usa_dynamic_row()
        row = usa_states[state_name]
        st = props["Status"]
        short = props["EventShortName"] + "|"
        if st == STATUS_PARKRUNNING:
            row["parkrunning"] += 1
            row["Total"] += 1
            row["events parkrunning"] += short
        elif st == STATUS_JUNIOR_PARKRUNNING:
            row["junior parkrunning"] += 1
            row["Total"] += 1
            row["events junior parkrunning"] += short
        elif st == STATUS_5K_CANCELLATION:
            row["5k Cancellations"] += 1
            row["Total"] += 1
            row["events 5k cancellation"] += short
        elif st == STATUS_JUNIOR_CANCELLATION:
            row["junior Cancellations"] += 1
            row["Total"] += 1
            row["events junior cancellation"] += short

    usa_states_od = collections.OrderedDict(sorted(usa_states.items()))
    usa_states = {}
    for k, v in usa_states_od.items():
        usa_states[k] = v

    usa_states["USA Total"] = countries["USA"]
    usa_states["USA Total"]["country"] = "USA"
    return usa_states
