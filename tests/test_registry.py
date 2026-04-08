"""countries_registry consistency and special-events merge snapshot."""

from parkrun_etl.aggregates import build_countries_shell
from parkrun_etl.countries_registry import (
    GLOBAL_COUNTRIES,
    SPECIAL_EVENTS_STEM_ORDER,
    build_countrycode_map,
    history_country_pairs,
    iter_display_names,
    validate_registry,
)
from parkrun_etl.history import HISTORY_COUNTRIES


def test_validate_registry_idempotent():
    validate_registry()


def test_history_matches_registry_and_total():
    assert HISTORY_COUNTRIES[0] == ("global.json", "Total")
    assert HISTORY_COUNTRIES[1:] == history_country_pairs()


def test_build_countries_shell_keys():
    shell = build_countries_shell()
    assert set(shell.keys()) == set(iter_display_names()) | {"Total"}


def test_countrycode_map_matches_registry_codes():
    m = build_countrycode_map()
    assert 85 not in m
    for r in GLOBAL_COUNTRIES:
        if r.countrycode is not None:
            assert m[r.countrycode] == (r.website_base, r.display_name)


def test_special_events_stem_group_snapshot():
    """Frozen membership + order defined in SPECIAL_EVENTS_STEM_ORDER."""
    stem_to_groups = {}
    for r in GLOBAL_COUNTRIES:
        if r.special_events is None:
            continue
        stem = r.special_events.html_stem
        stem_to_groups[stem] = r.special_events.merge_groups

    for group, ordered_stems in SPECIAL_EVENTS_STEM_ORDER.items():
        assert frozenset(ordered_stems) == frozenset(
            s for s, grps in stem_to_groups.items() if group in grps
        )
        for stem in ordered_stems:
            assert group in stem_to_groups[stem]
