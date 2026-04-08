import datetime
import json

from . import config
from .countries_registry import history_country_pairs
from .time_utils import now


def find_prior_datapoint(data_point, key):
    for i in range(-2, -100, -1):
        try:
            return data_point[i][key]
        except KeyError:
            pass
        except IndexError:
            return 0


# Legacy name (external scripts may still import).
findpendatapoint = find_prior_datapoint


def writehistory(history_file, history_data):
    """Write history history_data to history_file."""
    history_data["time"] = str(now())
    path = config.HISTORY_DIR / history_file
    try:
        with open(path, "r", encoding="utf-8", newline="\n") as f:
            old_data = json.loads(f.read())
        if now().weekday() == 0 and now().hour <= 1:
            olddate = datetime.datetime.strptime(
                old_data[-1]["time"], "%Y-%m-%d %H:%M:%S.%f"
            )
            if olddate.date() != now().date() and olddate.hour != now().hour:
                old_data = [old_data[-1], history_data]
    except FileNotFoundError:
        old_data = [
            {
                "parkrunning": 0,
                "junior parkrunning": 0,
                "5k Cancellations": 0,
                "junior Cancellations": 0,
                "Total": 0,
                "time": history_data["time"],
            }
        ]
    print(now(), "history/" + history_file + " read")
    last_data = old_data[-1]
    new_last_data = {}
    if last_data["parkrunning"] != history_data["parkrunning"] or find_prior_datapoint(
        old_data, "parkrunning"
    ) != history_data["parkrunning"]:
        new_last_data["parkrunning"] = last_data["parkrunning"]
    if last_data["junior parkrunning"] != history_data[
        "junior parkrunning"
    ] or find_prior_datapoint(old_data, "junior parkrunning") != history_data[
        "junior parkrunning"
    ]:
        new_last_data["junior parkrunning"] = last_data["junior parkrunning"]
    if last_data["5k Cancellations"] != history_data[
        "5k Cancellations"
    ] or find_prior_datapoint(old_data, "5k Cancellations") != history_data[
        "5k Cancellations"
    ]:
        new_last_data["5k Cancellations"] = last_data["5k Cancellations"]
    if last_data["junior Cancellations"] != history_data[
        "junior Cancellations"
    ] or find_prior_datapoint(old_data, "junior Cancellations") != history_data[
        "junior Cancellations"
    ]:
        new_last_data["junior Cancellations"] = last_data["junior Cancellations"]
    old_data.pop(-1)
    if len(new_last_data) != 0:
        new_last_data["Total"] = last_data["Total"]
        new_last_data["time"] = last_data["time"]
        old_data.append(new_last_data)
    new_data = {
        "parkrunning": history_data["parkrunning"],
        "junior parkrunning": history_data["junior parkrunning"],
        "5k Cancellations": history_data["5k Cancellations"],
        "junior Cancellations": history_data["junior Cancellations"],
        "Total": history_data["Total"],
        "time": history_data["time"],
    }
    old_data.append(new_data)
    with open(path, "wt", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(old_data, indent=4) + "\n")
    print(now(), "history/" + history_file + " saved")


HISTORY_COUNTRIES = [("global.json", "Total")] + history_country_pairs()

HISTORY_UK = [
    ("uk/england.json", "England"),
    ("uk/ni.json", "Northern Ireland"),
    ("uk/scotland.json", "Scotland"),
    ("uk/wales.json", "Wales"),
]

HISTORY_AUS = [
    ("aus/act.json", "Australian Capital Territory"),
    ("aus/nsw.json", "New South Wales"),
    ("aus/nt.json", "Northern Territory"),
    ("aus/qld.json", "Queensland"),
    ("aus/sa.json", "South Australia"),
    ("aus/tas.json", "Tasmania"),
    ("aus/vic.json", "Victoria"),
    ("aus/wa.json", "Western Australia"),
]


def write_all_history(countries, uk, aus, usa_states, usstateslist, _now_fn=None):
    for history_file, key in HISTORY_COUNTRIES:
        writehistory(history_file, countries[key])
    for history_file, key in HISTORY_UK:
        writehistory(history_file, uk[key])
    for history_file, key in HISTORY_AUS:
        writehistory(history_file, aus[key])
    for state in usstateslist:
        writehistory(
            "usa/" + state["code"] + ".json", usa_states[state["name"]]
        )
