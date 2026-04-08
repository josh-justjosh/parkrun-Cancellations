"""Write selected _data artifacts (paths and formats unchanged from legacy script)."""

import csv
import json


def write_reasons_json(reasons_dict, now_fn):
    with open('_data/reasons.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(reasons_dict, indent=2))
    print(now_fn(), 'reasons.json saved')


def write_events_geojson(events, now_fn):
    with open('_data/events.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(events, indent=2))
    print(now_fn(), 'events.json saved')


def write_cancellation_dates_tsv(cancellation_dates, now_fn):
    dates = list(dict.fromkeys(cancellation_dates))
    dates.sort()
    with open('_data/cancellation-dates.tsv', 'wt', encoding='utf-8', newline='') as f:
        tsv_writer = csv.writer(f, delimiter='\t')
        tsv_writer.writerow(['Dates'])
        for date in dates:
            tsv_writer.writerow([date])
    print(now_fn(), "cancellation-dates.tsv saved")
