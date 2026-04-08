"""Write selected _data artifacts (paths and formats unchanged from legacy script)."""

import csv
import json

from . import config

BREAKDOWN_HEADER = [
    "Country",
    "parkrunning",
    "junior parkrunning",
    "5k Cancellations",
    "junior Cancellations",
    "Total",
]

COUNTY_WIDE_HEADER = [
    "County",
    "parkrunning",
    "junior parkrunning",
    "5k Cancellations",
    "junior Cancellations",
    "Total",
    "5k Events Running",
    "junior Events Running",
    "5k Events Cancelled",
    "junior Events Cancelled",
]

COUNTY_ALL_HEADER = [
    "County",
    "Country",
    "parkrunning",
    "junior parkrunning",
    "5k Cancellations",
    "junior Cancellations",
    "Total",
    "5k Events Running",
    "junior Events Running",
    "5k Events Cancelled",
    "junior Events Cancelled",
]

USA_STATES_HEADER = [
    "States",
    "parkrunning",
    "junior parkrunning",
    "5k Cancellations",
    "junior Cancellations",
    "Total",
    "5k Events Running",
    "junior Events Running",
    "5k Events Cancelled",
    "junior Events Cancelled",
]


def write_reasons_json(reasons_dict, now_fn):
    with open(config.REASONS_JSON, "w", encoding="utf-8") as f:
        f.write(json.dumps(reasons_dict, indent=2))
    print(now_fn(), "reasons.json saved")


def write_events_geojson(events, now_fn):
    with open(config.EVENTS_JSON, "w", encoding="utf-8") as f:
        f.write(json.dumps(events, indent=2))
    print(now_fn(), "events.json saved")


def write_cancellation_dates_tsv(cancellation_dates, now_fn):
    dates = list(dict.fromkeys(cancellation_dates))
    dates.sort()
    with open(
        config.CANCELLATION_DATES_TSV, "wt", encoding="utf-8", newline=""
    ) as f:
        tsv_writer = csv.writer(f, delimiter="\t")
        tsv_writer.writerow(["Dates"])
        for date in dates:
            tsv_writer.writerow([date])
    print(now_fn(), "cancellation-dates.tsv saved")


def write_raw_events_json(text, now_fn):
    with open(config.RAW_EVENTS_JSON, "wt", encoding="utf-8", newline="") as f:
        f.write(text)
    print(now_fn(), "raw/events.json saved")


def write_raw_cancellations_html(html, now_fn):
    with open(
        config.RAW_CANCELLATIONS_HTML, "wt", encoding="utf-8", newline=""
    ) as f:
        f.write(html)
    print(now_fn(), "raw/cancellations.html saved")


def write_all_cancellations_tsv(cancellation_table, now_fn):
    with open(config.ALL_CANCELLATIONS_TSV, "wt", encoding="utf-8", newline="") as f:
        tsv_writer = csv.writer(f, delimiter="\t")
        tsv_writer.writerow(
            ["Date", "Event", "Region", "Country", "Cancellation Note"]
        )
        for row in cancellation_table:
            tsv_writer.writerow(row)
    print(now_fn(), "all-cancellations.tsv saved")


def write_events_table_tsv(events, now_fn):
    events_data = []
    for event in events["features"]:
        out = []
        props = event["properties"]
        geom = event["geometry"]["coordinates"]
        out.append(props["EventLongName"])
        out.append(geom[1])
        out.append(geom[0])
        out.append(props["Country"])
        out.append(props["State"])
        out.append(props["County"])
        out.append(props["Status"])
        out.append(props["Cancellations"])
        out.append(props["Website"])
        events_data.append(out)
    events_data.sort()
    with open(config.EVENTS_TABLE_TSV, "wt", encoding="utf-8", newline="") as f:
        tsv_writer = csv.writer(f, delimiter="\t")
        tsv_writer.writerow(
            [
                "Event",
                "Latitude",
                "Longitude",
                "Country",
                "State",
                "County",
                "Status",
                "Cancellations",
                "Website",
            ]
        )
        for event in events_data:
            tsv_writer.writerow(event)
    print(now_fn(), "events-table.tsv saved")


def write_breakdown_tsv(path, row_dict, now_fn, log_label):
    """Shared countries-data / uk-data / aus-data writer (non-zero cells only)."""
    with open(path, "wt", encoding="utf-8", newline="") as f:
        tsv_writer = csv.writer(f, delimiter="\t")
        tsv_writer.writerow(BREAKDOWN_HEADER)
        for i, j in row_dict.items():
            out = [i]
            for _k, l in j.items():
                if l != 0:
                    out.append(l)
                else:
                    out.append("")
            tsv_writer.writerow(out)
    print(now_fn(), log_label)


def write_uk_ie_county_subset_tsv(
    path,
    uk_ie_counties,
    country_filter,
    total_row_key,
    skip_value,
    now_fn,
    log_label,
):
    """One of england/ni/scotland/wales/ireland county exports."""
    with open(path, "wt", encoding="utf-8", newline="") as f:
        tsv_writer = csv.writer(f, delimiter="\t")
        tsv_writer.writerow(COUNTY_WIDE_HEADER)
        for i, j in uk_ie_counties.items():
            if j["country"] == country_filter:
                if i == total_row_key:
                    out = ["Total"]
                else:
                    out = [i]
                for k, l in j.items():
                    if l == skip_value:
                        pass
                    elif l not in [0, []]:
                        out.append(l)
                    else:
                        out.append("")
                if i == total_row_key:
                    for _x in range(4):
                        out.append("")
                tsv_writer.writerow(out)
    print(now_fn(), log_label)


def write_counties_all_tsv(uk_ie_counties, now_fn):
    path = config.COUNTIES_DIR / "all.tsv"
    with open(path, "wt", encoding="utf-8", newline="") as f:
        tsv_writer = csv.writer(f, delimiter="\t")
        tsv_writer.writerow(COUNTY_ALL_HEADER)
        for i, j in uk_ie_counties.items():
            out = [i]
            for k, l in j.items():
                if l not in [0, []]:
                    out.append(l)
                else:
                    out.append("")
            if "Total" in i:
                for _x in range(4):
                    out.append("")
            tsv_writer.writerow(out)
    print(now_fn(), "counties/all.tsv saved")


def write_usa_states_tsv(usa_states, now_fn):
    with open(config.USA_STATES_TSV, "wt", encoding="utf-8", newline="") as f:
        tsv_writer = csv.writer(f, delimiter="\t")
        tsv_writer.writerow(USA_STATES_HEADER)
        for i, j in usa_states.items():
            if j["country"] == "USA":
                if i == "USA Total":
                    out = ["USA"]
                else:
                    out = [i]
                for k, l in j.items():
                    if l == "USA":
                        pass
                    elif l not in [0, []]:
                        out.append(l)
                    else:
                        out.append("")
                if i == "USA Total":
                    for _x in range(4):
                        out.append("")
                tsv_writer.writerow(out)
    print(now_fn(), "usa-states.tsv saved")


def write_raw_states_tsv(new_states_list, now_fn):
    with open(config.RAW_STATES_TSV, "wt", encoding="utf-8", newline="") as f:
        tsv_writer = csv.writer(f, delimiter="\t")
        tsv_writer.writerow(["Event", "Country", "State", "County"])
        for event in new_states_list:
            tsv_writer.writerow(event)
    print(now_fn(), "raw/states.tsv saved")


def write_raw_ue_tsv(upcoming_events_table, now_fn):
    with open(config.RAW_UE_TSV, "wt", encoding="utf-8", newline="") as f:
        tsv_writer = csv.writer(f, delimiter="\t")
        tsv_writer.writerow(["Event", "Country"])
        for event in upcoming_events_table:
            tsv_writer.writerow([event[0], event[4]])
    print(now_fn(), "raw/ue.tsv saved")


def write_uk_ie_county_exports(uk_ie_counties, now_fn):
    write_uk_ie_county_subset_tsv(
        config.COUNTIES_DIR / "england.tsv",
        uk_ie_counties,
        "England",
        "England Total",
        "England",
        now_fn,
        "counties/england.tsv saved",
    )
    write_uk_ie_county_subset_tsv(
        config.COUNTIES_DIR / "ni.tsv",
        uk_ie_counties,
        "Northern Ireland",
        "NI Total",
        "Northern Ireland",
        now_fn,
        "counties/ni.tsv saved",
    )
    write_uk_ie_county_subset_tsv(
        config.COUNTIES_DIR / "scotland.tsv",
        uk_ie_counties,
        "Scotland",
        "Scotland Total",
        "Scotland",
        now_fn,
        "counties/scotland.tsv saved",
    )
    write_uk_ie_county_subset_tsv(
        config.COUNTIES_DIR / "wales.tsv",
        uk_ie_counties,
        "Wales",
        "Wales Total",
        "Wales",
        now_fn,
        "counties/wales.tsv saved",
    )
    write_uk_ie_county_subset_tsv(
        config.COUNTIES_DIR / "ireland.tsv",
        uk_ie_counties,
        "Ireland",
        "Ireland Total",
        "Ireland",
        now_fn,
        "counties/ireland.tsv saved",
    )
    write_counties_all_tsv(uk_ie_counties, now_fn)
