"""Lightweight regression tests for ETL helpers (no network)."""

import copy

from parkrun_etl.aggregates import (
    STATUS_5K_CANCELLATION,
    STATUS_JUNIOR_CANCELLATION,
    STATUS_PARKRUNNING,
    aggregate_by_country,
)
from parkrun_etl.country_codes import apply_country_website_and_country
from parkrun_etl.wiki_cancellations import parse_global_cancellations_table


def _feature(name, country, status, state="England", county=""):
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [0, 0]},
        "properties": {
            "EventLongName": name,
            "EventShortName": name.split()[0],
            "Country": country,
            "State": state,
            "County": county,
            "Status": status,
            "countrycode": 97,
        },
    }


def test_aggregate_by_country_mixed_statuses():
    features = [
        _feature("Alpha parkrun", "United Kingdom", STATUS_PARKRUNNING),
        _feature("Beta junior parkrun", "United Kingdom", STATUS_JUNIOR_CANCELLATION),
        _feature("Gamma parkrun", "Australia", STATUS_5K_CANCELLATION),
    ]
    countries = aggregate_by_country(features)
    assert countries["United Kingdom"]["parkrunning"] == 1
    assert countries["United Kingdom"]["junior Cancellations"] == 1
    assert countries["Australia"]["5k Cancellations"] == 1
    assert countries["Total"]["Total"] == 3


def test_apply_country_website_and_country_code_85_namibia():
    props = {
        "countrycode": 85,
        "EventLongName": "Windhoek parkrun",
        "Website": "",
        "Country": "",
    }
    apply_country_website_and_country(props)
    assert props["Country"] == "Namibia"
    assert props["Website"] == "https://www.parkrun.co.za/"


def test_apply_country_website_and_country_unknown_code():
    props = {
        "countrycode": 99999,
        "EventLongName": "X parkrun",
        "Website": "",
        "Country": "",
    }
    apply_country_website_and_country(props)
    assert props["Website"] == "Unavailable"


def test_apply_country_website_and_country_typical():
    props = copy.deepcopy(
        {
            "countrycode": 97,
            "EventLongName": "Test parkrun",
            "Website": "",
            "Country": "",
        }
    )
    apply_country_website_and_country(props)
    assert props["Country"] == "United Kingdom"
    assert props["Website"] == "https://www.parkrun.org.uk/"


def test_parse_global_cancellations_table_minimal_html():
    html = """
    <html><body>
    <table class="wikitable sortable">
    <tr><th>Date</th><th>Event</th><th>Region</th><th>Country</th><th>Note</th></tr>
    <tr>
      <td>2026-04-01</td><td>Example parkrun</td><td>x</td><td>UK</td><td>Weather</td>
    </tr>
    </table>
    </body></html>
    """
    rows = parse_global_cancellations_table(html)
    assert rows == [
        ["2026-04-01", "Example parkrun", "x", "UK", "Weather"],
    ]
