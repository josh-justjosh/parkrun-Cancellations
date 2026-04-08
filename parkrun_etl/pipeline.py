"""ETL pipeline: linear orchestration of fetch → enrich → aggregate → outputs."""

import collections
import csv
import json

import requests

from . import config
from .aggregates import (
    US_STATES_LIST,
    aggregate_aus_by_state,
    aggregate_by_country,
    aggregate_uk_by_nation,
    aggregate_uk_ie_counties,
    aggregate_usa_by_state,
)
from .cancellation_updates import apply_cancellation_updates
from .country_codes import apply_country_website_and_country
from .event_features import apply_map_popup_description, apply_special_day_flags
from .geo import resolve_new_event_state_county
from .history import write_all_history
from .http_headers import headers
from .outputs import (
    write_all_cancellations_tsv,
    write_breakdown_tsv,
    write_cancellation_dates_tsv,
    write_events_geojson,
    write_events_table_tsv,
    write_raw_cancellations_html,
    write_raw_events_json,
    write_raw_states_tsv,
    write_raw_ue_tsv,
    write_reasons_json,
    write_uk_ie_county_exports,
    write_usa_states_tsv,
)
from .special_events import load_special_events
from .table_utils import rem_dups, sort_by_index_0, sort_by_index_1
from .time_utils import now, same_week
from .wiki_cancellations import fetch_cancellations_wiki_html, parse_global_cancellations_table


def load_prior_state():
    """Read prior cancellations TSV and raw states TSV."""
    old_cancellations_data = []
    with open(config.CANCELLATIONS_TSV, "r", encoding="utf-8", newline="") as f:
        tsv_reader = csv.reader(f, delimiter="\t")
        for row in tsv_reader:
            row = rem_dups(row)
            old_cancellations_data.append(row)
    print(now(), "cancellations.tsv read")
    old_cancellations_data.remove(
        ["Date", "Event", "Country", "Cancellation Note", "Website"]
    )

    states_list = []
    with open(config.RAW_STATES_TSV, "r", encoding="utf-8", newline="") as f:
        tsv_reader = csv.reader(f, delimiter="\t")
        for row in tsv_reader:
            states_list.append(row)
    print(now(), "raw/states.tsv read")
    states_list.remove(["Event", "Country", "State", "County"])

    return states_list, old_cancellations_data


def fetch_events_and_wiki():
    """Download events.json and cancellations wiki HTML; persist raw copies."""
    events_text = requests.get(
        "https://images.parkrun.com/events.json", headers=headers, timeout=10
    ).text
    write_raw_events_json(
        json.dumps(json.loads(events_text), indent=2), now
    )

    print(now(), "getting cancellations data (wiki API parse, else index.php scoped table)")
    cancellations, cancellations_fetch_source = fetch_cancellations_wiki_html()
    print(now(), "cancellations HTML source:", cancellations_fetch_source)

    write_raw_cancellations_html(cancellations, now)

    events = json.loads(events_text)["events"]
    cancellation_table = parse_global_cancellations_table(cancellations)
    if not cancellation_table:
        print(
            now(),
            "WARNING: no cancellation rows parsed (empty table or parse failure)",
        )

    return events, cancellation_table, cancellations_fetch_source


def build_cancellation_views(cancellation_table):
    """Strip/sort wiki table rows; build same-week cancellations_data and reasons."""
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
            cancellations_data.append(
                [cancellation[0], cancellation[1], cancellation[3], cancellation[4]]
            )
            cancellations_list.append(cancellation[1])
            cancellation_reasons.append(cancellation[4])

    cancellation_reasons_count = collections.Counter(cancellation_reasons)
    cancellation_reasons_json = {i: j for i, j in cancellation_reasons_count.items()}

    write_reasons_json(cancellation_reasons_json, now)

    cancellation_table.sort(key=sort_by_index_0)
    cancellation_table.sort(key=sort_by_index_1)

    write_all_cancellations_tsv(cancellation_table, now)

    return cancellations_data, cancellations_list, cancellation_table


def enrich_features(
    events,
    cancellation_table,
    cancellations_list,
    states_list,
    cancellation_dates,
    new_states_list,
):
    """Walk GeoJSON features: status, cancellations, country/website, state/county, map text."""
    fetch_updates = False
    special_events = load_special_events(fetch_updates, headers, now)

    upcoming_events = []

    print(now(), "Upcoming Events:", upcoming_events)

    upcoming_set = set(upcoming_events)
    events["features"] = [
        f
        for f in events["features"]
        if f["properties"]["EventLongName"] not in upcoming_set
    ]

    for parkrun in events["features"]:
        if "junior" in parkrun["properties"]["EventLongName"]:
            if parkrun["properties"]["EventLongName"] in cancellations_list:
                parkrun["properties"]["Status"] = "junior Cancellation"
            else:
                parkrun["properties"]["Status"] = "junior parkrunning"
        else:
            if parkrun["properties"]["EventLongName"] in cancellations_list:
                parkrun["properties"]["Status"] = "5k Cancellation"
            else:
                parkrun["properties"]["Status"] = "parkrunning"

        parkrun["properties"]["Cancellations"] = []
        for cancellation in cancellation_table:
            if parkrun["properties"]["EventLongName"] == cancellation[1] and same_week(
                cancellation[0]
            ):
                newcancellation = {
                    "DateCancelled": cancellation[0],
                    "ReasonCancelled": cancellation[4],
                }
                parkrun["properties"]["Cancellations"].append(newcancellation)
                cancellation_dates.append(cancellation[0])

        apply_country_website_and_country(parkrun["properties"])

        if parkrun["properties"]["Website"] != "Unavailable":
            parkrun["properties"]["Website"] += parkrun["properties"]["eventname"]

        new = True
        for event in states_list:
            if event[0] == parkrun["properties"]["EventLongName"]:
                new_states_list.append(event)
                try:
                    parkrun["properties"]["State"] = event[2]
                except IndexError:
                    parkrun["properties"]["State"] = "-Unknown-"
                try:
                    parkrun["properties"]["County"] = event[3]
                except IndexError:
                    parkrun["properties"]["County"] = "-Unknown-"
                new = False

        if new:
            resolve_new_event_state_county(parkrun, headers, new_states_list, now)

        apply_map_popup_description(parkrun["properties"], now)

        apply_special_day_flags(parkrun["properties"], special_events)


def compute_and_write_aggregates(events):
    """
    Country/UK/AUS breakdown TSVs are written before USA aggregation, which mutates
    countries['USA'] (legacy shallow reference to usa_states['USA Total']).
    """
    features = events["features"]

    countries = aggregate_by_country(
        features,
        on_unknown_status=lambda name: print(now(), "Error:", name),
    )
    uk = aggregate_uk_by_nation(features)
    aus = aggregate_aus_by_state(
        features,
        log_fn=lambda name, msg: print(now(), name, msg),
    )

    write_breakdown_tsv(
        config.COUNTRIES_DATA_TSV, countries, now, "countries-data.tsv saved"
    )
    write_breakdown_tsv(config.UK_DATA_TSV, uk, now, "uk-data.tsv saved")
    write_breakdown_tsv(config.AUS_DATA_TSV, aus, now, "aus-data.tsv saved")

    uk_ie_counties = aggregate_uk_ie_counties(features)
    usa_states = aggregate_usa_by_state(features, countries)

    write_uk_ie_county_exports(uk_ie_counties, now)
    write_usa_states_tsv(usa_states, now)

    return countries, uk, aus, uk_ie_counties, usa_states


def run():
    print(now(), "Script Start")

    states_list, old_cancellations_data = load_prior_state()

    events, cancellation_table, _source = fetch_events_and_wiki()

    cancellations_data, cancellations_list, cancellation_table = build_cancellation_views(
        cancellation_table
    )

    cancellation_dates = []
    new_states_list = []

    enrich_features(
        events,
        cancellation_table,
        cancellations_list,
        states_list,
        cancellation_dates,
        new_states_list,
    )

    write_events_geojson(events, now)
    write_cancellation_dates_tsv(cancellation_dates, now)
    write_events_table_tsv(events, now)

    countries, uk, aus, uk_ie_counties, usa_states = compute_and_write_aggregates(
        events
    )

    apply_cancellation_updates(
        old_cancellations_data, cancellations_data, events, now
    )

    write_raw_states_tsv(new_states_list, now)

    upcoming_events_table = []
    upcoming_events_table.sort()
    write_raw_ue_tsv(upcoming_events_table, now)

    write_all_history(countries, uk, aus, usa_states, US_STATES_LIST)

    print(now(), "Script End")
