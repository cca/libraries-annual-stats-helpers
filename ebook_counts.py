#!/usr/bin/env python3
# /// script
# dependencies = ["python-dateutil"]
# ///
"""
Sum ebook usage statistics from COUNTER 5 Platform Reports downloaded in bulk via the COUNTER 5 Report Tool.
This script can be used to fill out the SCELC/OAPEN ebook pilot survey, e.g. by running it like:
./ebook_counts.py 2022-10 2023-01
make sure we have all the data for the months we want to report on first.
"""

import argparse
import json
import os
from datetime import date

from dateutil.relativedelta import relativedelta

data = {
    "Platforms": {},
    "Totals": {},
}


def add_or_init(platform, metric, count):
    """Add to an existing category in the data dict
    or initialize one if it does not already exist.

    Args:
        platform (str): vendor platform, e.g. "ProQuest"
        metric (str): type of usage metric, e.g. "Unique_Item_Requests"
        count (int): count of usage metric, e.g. 23
    """
    global data

    # case 1: platform does not yet exist
    if not data["Platforms"].get(platform, False):
        data["Platforms"][platform] = {metric: count}
    # case 2: we have the platform but not the metric
    elif not data["Platforms"][platform].get(metric, False):
        data["Platforms"][platform][metric] = count
    # case 3: we have the platform and the metric, just need to add to the total
    else:
        data["Platforms"][platform][metric] += count

    # do the same process but for the totals
    if not data["Totals"].get(metric, False):
        data["Totals"][metric] = count
    else:
        data["Totals"][metric] += count


def process_year(year, start_date, end_date):
    for root, dirs, files in os.walk(f".DO_NOT_MODIFY/_json/{year}"):
        for name in files:
            if name.endswith("_TR_B1.json"):
                print("Processing report {}".format(name))
                with open(os.path.join(root, name), "r") as fh:
                    report = json.load(fh)
                    for item in report.get("Report_Items", []):
                        platform = item["Platform"]
                        for period in item["Performance"]:
                            if (
                                date.fromisoformat(period["Period"]["Begin_Date"])
                                >= start_date
                                and date.fromisoformat(period["Period"]["End_Date"])
                                < end_date
                            ):
                                for instance in period["Instance"]:
                                    add_or_init(
                                        platform,
                                        instance["Metric_Type"],
                                        instance["Count"],
                                    )


def main(sd, ed):
    start_date = date(int(sd.split("-")[0]), int(sd.split("-")[1]), 1)
    end_date = date(int(ed.split("-")[0]), int(ed.split("-")[1]), 1)
    end_date += relativedelta(months=1)
    years = set()
    years.add(start_date.year)
    years.add(end_date.year)
    for year in years:
        process_year(year, start_date, end_date)

    filename = f"{sd}-to-{ed}-ebooks.json"
    with open(filename, "w") as fh:
        json.dump(data, fh, indent=2, sort_keys=True)
    print(f"Wrote results to {filename}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Aggregate usage statistics from COUNTER 5 Platform Reports downloaded in bulk via the COUNTER 5 Report Tool."
    )
    parser.add_argument(
        "start_date", metavar="YYYY-MM", type=str, nargs=1, help="start month (YYYY-MM)"
    )
    parser.add_argument(
        "end_date",
        metavar="YYYY-MM",
        type=str,
        nargs=1,
        help="end month (YYYY-MM), inclusive",
    )
    args = parser.parse_args()
    main(args.start_date[0], args.end_date[0])
