"""Fetch and parse parkrun special-events HTML (Christmas/NYD etc.)."""
import json

import requests
from bs4 import BeautifulSoup
from html_table_extractor.extractor import Extractor

from .config import SPECIAL_EVENTS_DIR, SPECIAL_EVENTS_JSON
from .countries_registry import (
    SPECIAL_EVENTS_STEM_ORDER,
    SpecialEventsMergeGroup,
    iter_special_events_sources,
)


def _parse_table_from_path(path):
    with open(path, "r", encoding="utf-8", newline="\n") as f:
        soup = BeautifulSoup(f, "html.parser")
    extractor = Extractor(soup)
    extractor.parse()
    table = extractor.return_list()
    table.pop(0)
    return table


def _concat_merge_group(tables_by_stem, group: SpecialEventsMergeGroup):
    out = []
    for stem in SPECIAL_EVENTS_STEM_ORDER[group]:
        out.extend(tables_by_stem[stem])
    return out


def load_special_events(fetch_updates, headers, now_fn):
    special_events = []
    if not fetch_updates:
        return special_events

    tables_by_stem = {}

    for src in iter_special_events_sources():
        path = SPECIAL_EVENTS_DIR / f"{src.html_stem}.html"
        if fetch_updates:
            html = requests.get(src.fetch_url, headers=headers, timeout=10).text
            with open(path, "wt", encoding="utf-8", newline="") as f:
                f.write(html)
            print(now_fn(), f"_data/special_events/{src.html_stem}.html saved")
        tables_by_stem[src.html_stem] = _parse_table_from_path(path)

    se_table1 = _concat_merge_group(
        tables_by_stem, SpecialEventsMergeGroup.CHRISTMAS_NYD
    )
    se_table1.sort()
    for row in se_table1:
        out = {}
        out["EventLongName"] = row[0]
        if row[2] == "❌":
            out["2024-12-25"] = False
        elif row[2] == "✅":
            out["2024-12-25"] = True

        if row[3] == "❌":
            out["2025-01-01"] = False
        elif row[3] == "✅":
            out["2025-01-01"] = True

        special_events.append(out)

    se_table2 = _concat_merge_group(tables_by_stem, SpecialEventsMergeGroup.NYD_ONLY)
    se_table2.sort()
    for row in se_table2:
        out = {}
        out["EventLongName"] = row[0]
        if row[2] == "❌":
            out["2025-01-01"] = False
        elif row[2] == "✅":
            out["2025-01-01"] = True

        special_events.append(out)

    se_table3 = _concat_merge_group(tables_by_stem, SpecialEventsMergeGroup.BOXING_NYD)
    for row in se_table3:
        out = {}
        out["EventLongName"] = row[0]
        if row[2] == "❌":
            out["2024-12-26"] = False
        elif row[2] == "✅":
            out["2024-12-26"] = True

        if row[3] == "❌":
            out["2025-01-01"] = False
        elif row[3] == "✅":
            out["2025-01-01"] = True

        special_events.append(out)

    se_table4 = _concat_merge_group(
        tables_by_stem, SpecialEventsMergeGroup.THANKSGIVING
    )
    for row in se_table4:
        out = {}
        out["EventLongName"] = row[0]
        if row[2] == "❌":
            out["2024-11-28"] = False
        elif row[2] == "✅":
            out["2024-11-28"] = True

        if row[3] == "❌":
            out["2025-01-01"] = False
        elif row[3] == "✅":
            out["2025-01-01"] = True

        special_events.append(out)

    with open(SPECIAL_EVENTS_JSON, "wt", encoding="utf-8", newline="") as f:
        f.write(json.dumps(special_events, indent=2))
        print(now_fn(), "special_events.json saved")
