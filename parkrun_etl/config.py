"""Central paths for ETL outputs (relative to repo root / cwd)."""

from pathlib import Path

DATA_DIR = Path("_data")
RAW_DIR = DATA_DIR / "raw"
HISTORY_DIR = DATA_DIR / "history"
COUNTIES_DIR = DATA_DIR / "counties"
SPECIAL_EVENTS_DIR = DATA_DIR / "special_events"
POSTS_CANCELLATION_UPDATES = Path("_posts") / "Cancellation Updates"

CANCELLATIONS_TSV = DATA_DIR / "cancellations.tsv"
RAW_STATES_TSV = RAW_DIR / "states.tsv"
RAW_EVENTS_JSON = RAW_DIR / "events.json"
RAW_CANCELLATIONS_HTML = RAW_DIR / "cancellations.html"
ALL_CANCELLATIONS_TSV = DATA_DIR / "all-cancellations.tsv"
EVENTS_TABLE_TSV = DATA_DIR / "events-table.tsv"
COUNTRIES_DATA_TSV = DATA_DIR / "countries-data.tsv"
UK_DATA_TSV = DATA_DIR / "uk-data.tsv"
AUS_DATA_TSV = DATA_DIR / "aus-data.tsv"
USA_STATES_TSV = DATA_DIR / "usa-states.tsv"
REASONS_JSON = DATA_DIR / "reasons.json"
EVENTS_JSON = DATA_DIR / "events.json"
CANCELLATION_DATES_TSV = DATA_DIR / "cancellation-dates.tsv"
CANCELLATION_ADDITIONS_TSV = DATA_DIR / "cancellation-additions.tsv"
CANCELLATION_REMOVALS_TSV = DATA_DIR / "cancellation-removals.tsv"
CANCELLATION_CHANGES_TSV = DATA_DIR / "cancellation-changes.tsv"
RAW_UE_TSV = RAW_DIR / "ue.tsv"
SPECIAL_EVENTS_JSON = DATA_DIR / "special_events.json"
