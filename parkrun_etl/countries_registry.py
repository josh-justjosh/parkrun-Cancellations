"""
Single source of truth for global countries: display name, history file, countrycode map,
website base, and optional special-events fetch/merge metadata.

Countrycode 85 is shared by Namibia, Eswatini, and South Africa (event-name split in
apply_country_website_and_country); those three rows use countrycode=None here so they are
not inserted into COUNTRYCODE_MAP — only the cc == 85 branch assigns them.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, FrozenSet, Iterator, List, Tuple

# Event long names that use countrycode 85 but map to Namibia / Eswatini (rest → South Africa).
NAMIBIA_EVENTS = frozenset(
    [
        "Windhoek parkrun",
        "Omeya parkrun",
        "Swakopmund parkrun",
        "Walvis Bay parkrun",
    ]
)
ESWATINI_EVENTS = frozenset(
    [
        "Mbabane parkrun",
        "Manzini parkrun",
    ]
)

CODE_85_WEBSITE_BASE = "https://www.parkrun.co.za/"


class SpecialEventsMergeGroup(str, Enum):
    """Which special_events.json merge pipeline a cached HTML table feeds."""

    CHRISTMAS_NYD = "christmas_nyd"
    NYD_ONLY = "nyd_only"
    BOXING_NYD = "boxing_nyd"
    THANKSGIVING = "thanksgiving"


# Concat order within each merged table (must match legacy special_events.py).
SPECIAL_EVENTS_STEM_ORDER: Dict[SpecialEventsMergeGroup, Tuple[str, ...]] = {
    SpecialEventsMergeGroup.CHRISTMAS_NYD: ("au", "fr", "ie", "it", "nz", "uk"),
    SpecialEventsMergeGroup.NYD_ONLY: (
        "ca",
        "dk",
        "fi",
        "de",
        "jp",
        "my",
        "nl",
        "no",
        "sg",
        "za",
        "se",
        "lt",
    ),
    SpecialEventsMergeGroup.BOXING_NYD: ("pl",),
    SpecialEventsMergeGroup.THANKSGIVING: ("us",),
}


@dataclass(frozen=True)
class SpecialEventsSource:
    fetch_url: str
    html_stem: str
    merge_groups: FrozenSet[SpecialEventsMergeGroup]

    def __post_init__(self) -> None:
        if not self.merge_groups:
            raise ValueError("merge_groups must be non-empty")


@dataclass(frozen=True)
class CountryRecord:
    display_name: str
    history_basename: str
    countrycode: int | None
    website_base: str
    special_events: SpecialEventsSource | None = None


def _se(
    url: str, stem: str, *groups: SpecialEventsMergeGroup
) -> SpecialEventsSource:
    return SpecialEventsSource(
        fetch_url=url, html_stem=stem, merge_groups=frozenset(groups)
    )


# Order matches legacy countries-data.tsv / build_countries_shell.
GLOBAL_COUNTRIES: Tuple[CountryRecord, ...] = (
    CountryRecord(
        "Australia",
        "australia.json",
        3,
        "https://www.parkrun.com.au/",
        _se(
            "https://www.parkrun.com.au/special-events",
            "au",
            SpecialEventsMergeGroup.CHRISTMAS_NYD,
        ),
    ),
    CountryRecord("Austria", "austria.json", 4, "https://www.parkrun.co.at/"),
    CountryRecord(
        "Canada",
        "canada.json",
        14,
        "https://www.parkrun.ca/",
        _se(
            "https://www.parkrun.ca/special-events",
            "ca",
            SpecialEventsMergeGroup.NYD_ONLY,
        ),
    ),
    CountryRecord(
        "Denmark",
        "denmark.json",
        23,
        "https://www.parkrun.dk/",
        _se(
            "https://www.parkrun.dk/special-events",
            "dk",
            SpecialEventsMergeGroup.NYD_ONLY,
        ),
    ),
    CountryRecord(
        "Eswatini",
        "eswatini.json",
        None,
        CODE_85_WEBSITE_BASE,
    ),
    CountryRecord(
        "Finland",
        "finland.json",
        30,
        "https://www.parkrun.fi/",
        _se(
            "https://www.parkrun.fi/special-events",
            "fi",
            SpecialEventsMergeGroup.NYD_ONLY,
        ),
    ),
    CountryRecord(
        "France",
        "france.json",
        31,
        "https://www.parkrun.fr/",
        _se(
            "https://www.parkrun.fr/special-events",
            "fr",
            SpecialEventsMergeGroup.CHRISTMAS_NYD,
        ),
    ),
    CountryRecord(
        "Germany",
        "germany.json",
        32,
        "https://www.parkrun.com.de/",
        _se(
            "https://www.parkrun.com.de/special-events",
            "de",
            SpecialEventsMergeGroup.NYD_ONLY,
        ),
    ),
    CountryRecord(
        "Ireland",
        "ireland.json",
        42,
        "https://www.parkrun.ie/",
        _se(
            "https://www.parkrun.ie/special-events",
            "ie",
            SpecialEventsMergeGroup.CHRISTMAS_NYD,
        ),
    ),
    CountryRecord(
        "Italy",
        "italy.json",
        44,
        "https://www.parkrun.it/",
        _se(
            "https://www.parkrun.it/special-events",
            "it",
            SpecialEventsMergeGroup.CHRISTMAS_NYD,
        ),
    ),
    CountryRecord(
        "Japan",
        "japan.json",
        46,
        "https://www.parkrun.jp/",
        _se(
            "https://www.parkrun.jp/special-events",
            "jp",
            SpecialEventsMergeGroup.NYD_ONLY,
        ),
    ),
    CountryRecord(
        "Lithuania",
        "lithuania.json",
        54,
        "https://www.parkrun.lt/",
        _se(
            "https://www.parkrun.lt/special-events",
            "lt",
            SpecialEventsMergeGroup.NYD_ONLY,
        ),
    ),
    CountryRecord(
        "Malaysia",
        "malaysia.json",
        57,
        "https://www.parkrun.my/",
        _se(
            "https://www.parkrun.my/special-events",
            "my",
            SpecialEventsMergeGroup.NYD_ONLY,
        ),
    ),
    CountryRecord(
        "Namibia",
        "namibia.json",
        None,
        CODE_85_WEBSITE_BASE,
    ),
    CountryRecord(
        "Netherlands",
        "netherlands.json",
        64,
        "https://www.parkrun.co.nl/",
        _se(
            "https://www.parkrun.co.nl/special-events",
            "nl",
            SpecialEventsMergeGroup.NYD_ONLY,
        ),
    ),
    CountryRecord(
        "New Zealand",
        "newzealand.json",
        65,
        "https://www.parkrun.co.nz/",
        _se(
            "https://www.parkrun.co.nz/special-events",
            "nz",
            SpecialEventsMergeGroup.CHRISTMAS_NYD,
        ),
    ),
    CountryRecord(
        "Norway",
        "norway.json",
        67,
        "https://www.parkrun.no/",
        _se(
            "https://www.parkrun.no/special-events",
            "no",
            SpecialEventsMergeGroup.NYD_ONLY,
        ),
    ),
    CountryRecord(
        "Poland",
        "poland.json",
        74,
        "https://www.parkrun.pl/",
        _se(
            "https://www.parkrun.pl/special-events",
            "pl",
            SpecialEventsMergeGroup.BOXING_NYD,
        ),
    ),
    CountryRecord("Russia", "russia.json", 79, "https://www.parkrun.ru/"),
    CountryRecord(
        "Singapore",
        "singapore.json",
        82,
        "https://www.parkrun.sg/",
        _se(
            "https://www.parkrun.sg/special-events",
            "sg",
            SpecialEventsMergeGroup.NYD_ONLY,
        ),
    ),
    CountryRecord(
        "South Africa",
        "southafrica.json",
        None,
        CODE_85_WEBSITE_BASE,
        _se(
            "https://www.parkrun.co.za/special-events",
            "za",
            SpecialEventsMergeGroup.NYD_ONLY,
        ),
    ),
    CountryRecord(
        "Sweden",
        "sweden.json",
        88,
        "https://www.parkrun.se/",
        _se(
            "https://www.parkrun.se/special-events",
            "se",
            SpecialEventsMergeGroup.NYD_ONLY,
        ),
    ),
    CountryRecord(
        "United Kingdom",
        "unitedkingdom.json",
        97,
        "https://www.parkrun.org.uk/",
        _se(
            "https://www.parkrun.org.uk/special-events",
            "uk",
            SpecialEventsMergeGroup.CHRISTMAS_NYD,
        ),
    ),
    CountryRecord(
        "USA",
        "unitedstates.json",
        98,
        "https://www.parkrun.us/",
        _se(
            "https://www.parkrun.us/special-events",
            "us",
            SpecialEventsMergeGroup.THANKSGIVING,
        ),
    ),
)


def iter_display_names() -> Iterator[str]:
    for r in GLOBAL_COUNTRIES:
        yield r.display_name


def history_country_pairs() -> List[Tuple[str, str]]:
    return [(r.history_basename, r.display_name) for r in GLOBAL_COUNTRIES]


def build_countrycode_map() -> Dict[int, Tuple[str, str]]:
    out: Dict[int, Tuple[str, str]] = {}
    for r in GLOBAL_COUNTRIES:
        if r.countrycode is None:
            continue
        out[r.countrycode] = (r.website_base, r.display_name)
    return out


def iter_special_events_sources() -> Iterator[SpecialEventsSource]:
    """Registry order; each stem appears once (first occurrence wins if duplicated)."""
    seen: set[str] = set()
    for r in GLOBAL_COUNTRIES:
        if r.special_events is None:
            continue
        stem = r.special_events.html_stem
        if stem in seen:
            continue
        seen.add(stem)
        yield r.special_events


def validate_registry() -> None:
    names = [r.display_name for r in GLOBAL_COUNTRIES]
    if len(set(names)) != len(names):
        raise ValueError("duplicate display_name in GLOBAL_COUNTRIES")

    hist = [r.history_basename for r in GLOBAL_COUNTRIES]
    if len(set(hist)) != len(hist):
        raise ValueError("duplicate history_basename in GLOBAL_COUNTRIES")

    codes = [r.countrycode for r in GLOBAL_COUNTRIES if r.countrycode is not None]
    if len(set(codes)) != len(codes):
        raise ValueError("duplicate countrycode in GLOBAL_COUNTRIES")

    stems: List[str] = []
    stem_to_groups: Dict[str, FrozenSet[SpecialEventsMergeGroup]] = {}
    for r in GLOBAL_COUNTRIES:
        if r.special_events is None:
            continue
        s = r.special_events.html_stem
        if "/" in s or "\\" in s or ".." in s:
            raise ValueError(f"unsafe html_stem: {s!r}")
        stems.append(s)
        if s in stem_to_groups:
            if stem_to_groups[s] != r.special_events.merge_groups:
                raise ValueError(f"inconsistent merge_groups for stem {s!r}")
        else:
            stem_to_groups[s] = r.special_events.merge_groups

    if len(set(stems)) != len(stems):
        raise ValueError("duplicate special_events html_stem in GLOBAL_COUNTRIES")

    for group, ordered in SPECIAL_EVENTS_STEM_ORDER.items():
        expected = frozenset(ordered)
        found = frozenset(s for s, g in stem_to_groups.items() if group in g)
        if found != expected:
            raise ValueError(
                f"special events stems for {group}: expected {expected!r}, got {found!r}"
            )


validate_registry()
