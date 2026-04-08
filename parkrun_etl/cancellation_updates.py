"""Diff prior vs current cancellations and write TSVs / optional Jekyll update post."""

import csv

from . import config
from .table_utils import rem_dups, sort_by_index_0, sort_by_index_1


def _pad_dt_part(n):
    n = int(n)
    return "0" + str(n) if n < 10 else str(n)


def apply_cancellation_updates(
    old_cancellations_data,
    cancellations_data,
    events,
    now_fn,
):
    """
    Mutates cancellations_data (adds Website), sorts, writes cancellations.tsv and
    optional diff TSVs + markdown post. Mirrors legacy cli behaviour.
    """
    cancellations_changes = []
    cancellations_additions = []
    cancellations_removals = []

    for i in old_cancellations_data:
        try:
            oldwebsite = i[4]
            i.pop(4)
        except IndexError:
            oldwebsite = None
        if i not in cancellations_data:
            out = i
            for parkrun in events["features"]:
                if parkrun["properties"]["EventLongName"] == i[1]:
                    out.append(oldwebsite)
                    break
            cancellations_removals.append(out)

    for i in cancellations_data:
        if i not in old_cancellations_data:
            out = i
            for parkrun in events["features"]:
                if parkrun["properties"]["EventLongName"] == i[1]:
                    out.append(parkrun["properties"]["Website"])
                    break
            cancellations_additions.append(out)

    for cancellation in cancellations_data:
        if len(cancellation) <= 4:
            out = ""
            for parkrun in events["features"]:
                if parkrun["properties"]["EventLongName"] == cancellation[1]:
                    out = parkrun["properties"]["Website"]
                    break
            cancellation.append(out)
            cancellation = rem_dups(cancellation)

    cancellations_additions.sort()
    cancellations_removals.sort()
    cancellations_data.sort(key=sort_by_index_0)
    cancellations_data.sort(key=sort_by_index_1)

    with open(config.CANCELLATIONS_TSV, "wt", encoding="utf-8", newline="") as f:
        tsv_writer = csv.writer(f, delimiter="\t")
        tsv_writer.writerow(
            ["Date", "Event", "Country", "Cancellation Note", "Website"]
        )
        for event in cancellations_data:
            tsv_writer.writerow(event)
    print(now_fn(), "cancellations.tsv saved")

    if cancellations_additions:
        with open(
            config.CANCELLATION_ADDITIONS_TSV, "wt", encoding="utf-8", newline=""
        ) as f:
            tsv_writer = csv.writer(f, delimiter="\t")
            tsv_writer.writerow(
                ["Date", "Event", "Country", "Cancellation Note", "Website"]
            )
            for event in cancellations_additions:
                tsv_writer.writerow(event)
                event.append("Added")
                cancellations_changes.append(event)
            tsv_writer.writerow([now_fn(), "", "", ""])
        print(now_fn(), "cancellation-additions.tsv saved")

    if cancellations_removals:
        with open(
            config.CANCELLATION_REMOVALS_TSV, "wt", encoding="utf-8", newline=""
        ) as f:
            tsv_writer = csv.writer(f, delimiter="\t")
            tsv_writer.writerow(
                [
                    "Date",
                    "Event",
                    "Country",
                    "Previous Cancellation Note",
                    "Website",
                ]
            )
            for event in cancellations_removals:
                tsv_writer.writerow(event)
                event.append("Removed")
                cancellations_changes.append(event)
            tsv_writer.writerow([now_fn(), "", "", ""])
        print(now_fn(), "cancellation-removals.tsv saved")

    cancellations_changes.sort()

    if cancellations_changes:
        with open(
            config.CANCELLATION_CHANGES_TSV, "wt", encoding="utf-8", newline=""
        ) as f:
            tsv_writer = csv.writer(f, delimiter="\t")
            tsv_writer.writerow(
                [
                    "Date",
                    "Event",
                    "Country",
                    "Cancellation Note",
                    "Website",
                    "Added or Removed",
                ]
            )
            for event in cancellations_changes:
                tsv_writer.writerow(event)
            tsv_writer.writerow([now_fn(), "", "", "", ""])
        print(now_fn(), "cancellation-changes.tsv saved")

        now_saved = now_fn()
        month = _pad_dt_part(now_saved.month)
        day = _pad_dt_part(now_saved.day)
        hour = _pad_dt_part(now_saved.hour)
        minute = _pad_dt_part(now_saved.minute)
        second = _pad_dt_part(now_saved.second)

        filename = (
            f"{now_saved.year}-{month}-{day}-"
            f"{hour}{minute}{second}-update.md"
        )
        post_path = config.POSTS_CANCELLATION_UPDATES / filename
        with open(post_path, "w+", encoding="utf-8", newline="") as f:
            out = "---" + "\n"
            out += "layout: post" + "\n"
            out += (
                "title: "
                + str(now_saved.year)
                + "/"
                + month
                + "/"
                + day
                + " "
                + hour
                + ":"
                + minute
                + " UTC Update"
                + "\n"
            )
            out += (
                "date: "
                + str(now_saved.year)
                + "-"
                + month
                + "-"
                + day
                + " "
                + hour
                + ":"
                + minute
                + ":"
                + second
                + " +0000"
                + "\n"
            )
            out += "author: Cancellations Bot" + "\n"
            out += "category: 'Cancellation Update'" + "\n\n"
            out += "---" + "\n"
            out += "\n"
            if cancellations_additions:
                out += "<h3>New Cancellations</h3>" + "\n"
                out += "<div class='hscrollable'>" + "\n"
                out += "<table style='width: 100%'>" + "\n"
                out += "    <tr>" + "\n"
                out += "        <th>Event</th>" + "\n"
                out += "        <th>Country</th>" + "\n"
                out += "        <th>Date</th>" + "\n"
                out += "        <th>Cancellation Note</th>" + "\n"
                out += "    </tr>" + "\n"
                for event in cancellations_additions:
                    out += "    <tr>" + "\n"
                    if event[4] not in ["", "Added"]:
                        out += (
                            "        <td><a href=\""
                            + event[4]
                            + '">'
                            + event[1]
                            + "</a></td>"
                            + "\n"
                        )
                    else:
                        out += "        <td>" + event[1] + "</td>" + "\n"
                    out += "        <td>" + event[2] + "</td>" + "\n"
                    out += "        <td>" + event[0] + "</td>" + "\n"
                    out += "        <td>" + event[3] + "</td>" + "\n"
                    out += "    </tr>" + "\n"
                out += "</table>" + "\n"
                out += "</div>" + "\n"
            if cancellations_removals:
                out += "<h3>Cancellations Removed</h3>" + "\n"
                out += "<div class='hscrollable'>" + "\n"
                out += "<table style='width: 100%'>" + "\n"
                out += "    <tr>" + "\n"
                out += "        <th>Event</th>" + "\n"
                out += "        <th>Country</th>" + "\n"
                out += "        <th>Date</th>" + "\n"
                out += "        <th>Previous Cancellation Note</th>" + "\n"
                out += "    </tr>" + "\n"
                for event in cancellations_removals:
                    out += "    <tr>" + "\n"
                    if event[4] not in ["", "Removed"]:
                        out += (
                            "        <td><a href=\""
                            + event[4]
                            + '">'
                            + event[1]
                            + "</a></td>"
                            + "\n"
                        )
                    else:
                        out += "        <td>" + event[1] + "</td>" + "\n"
                    out += "        <td>" + event[2] + "</td>" + "\n"
                    out += "        <td>" + event[0] + "</td>" + "\n"
                    out += "        <td>" + event[3] + "</td>" + "\n"
                    out += "    </tr>" + "\n"
                out += "</table>" + "\n"
                out += "</div>" + "\n"

            f.write(out)
        print(now_fn(), filename, "saved")
