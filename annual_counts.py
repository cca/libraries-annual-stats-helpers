#!/usr/bin/env python3
"""
Summarize a year's worth of COUNTER usage statistics.
The data is stored in the COUNTER 5 Reports Tool app's "all_data" folder
which this script expects to exist in an "all_data" directory under your user's
home. You must run that tool before summarizing the reports.

NOTE: the canonical version of this script lives in libraries-annual-stats-helpers repo
https://github.com/cca/libraries-annual-stats-helpers
and changes to it should be tracked there.
"""
import argparse
import json
import os
from pathlib import Path
from typing import Any, Callable

data: dict[str, Any] = {
    "Platforms": {},
    "Resource Types": {},
    "Aggregated Resource Types": {
        "eBooks": 0,
        "Multimedia": 0,
        "Other": 0,
        "Periodicals": 0,
        "Total": 0,
    },
}


def add_or_init(platform: str, dtype: str, metric: str, count: int) -> None:
    """Add to an existing category in the data dict
    or initialize one if it does not already exist.

    Args:
        platform (str): vendor platform, e.g. "ProQuest"
        dtype (str): data type from COUNTER report, e.g. "Book"
        metric (str): usage type from COUNTER report, e.g. "Unique_Item_Requests"
        count (int): count of usage metric, e.g. 23
    """
    global data

    # print info about Multimedia data
    if dtype == "Multimedia" and os.environ.get("DEBUG"):
        print("Found {} {} for type {} on {}".format(count, metric, dtype, platform))

    # case 1: platform does not yet exist
    if not data["Platforms"].get(platform, False):
        data["Platforms"][platform] = {metric: count}
    # case 2: we have the platform but not this particular metric
    elif not data["Platforms"][platform].get(metric, False):
        data["Platforms"][platform][metric] = count
    # case 3: we have both & just need to add to the total
    else:
        data["Platforms"][platform][metric] += count

    if not data["Resource Types"].get(dtype, False):
        data["Resource Types"][dtype] = {metric: count}
    elif not data["Resource Types"][dtype].get(metric, False):
        data["Resource Types"][dtype][metric] = count
    else:
        data["Resource Types"][dtype][metric] += count


def counter5(report: dict[str, Any]) -> None:
    for item in report.get("Report_Items", []):
        dtype: str = item["Data_Type"]
        platform: str = item["Platform"]
        for period in item["Performance"]:
            for instance in period["Instance"]:
                metric: str = instance["Metric_Type"]
                count: int = instance["Count"]
                if os.environ.get("DEBUG"):
                    print(
                        "{} {} for type {} on {}".format(count, metric, dtype, platform)
                    )
                add_or_init(platform, dtype, metric, count)


def counter51(report: dict[str, Any]) -> None:
    for item in report.get("Report_Items", []):
        platform: str = item["Platform"]
        for attr_perf in item["Attribute_Performance"]:
            dtype: str = attr_perf["Data_Type"]
            for metric in attr_perf["Performance"]:
                count: int = sum(attr_perf["Performance"][metric].values())
                if os.environ.get("DEBUG"):
                    print(
                        "{} {} for type {} on {}".format(count, metric, dtype, platform)
                    )
                add_or_init(platform, dtype, metric, count)


counter_parsers: dict[str, Callable] = {"5": counter5, "5.1": counter51}


def calc_aggregated(data) -> None:
    """Combine media categories to receive an aggregated total

    Args:
        data (dict): data object populated from COUNTER reports (see top of this file)

    2023 IPEDS guidance: different platform types use different metrics for their totals.
    - Ebooks: BR_T1 use unique title request
    - Multimedia: IR_M1 use total item request
    - E-serial: TR_J1 use unique title request

    For now we are just using total item requests across the board but putting this here for future reference.
    """
    # TODO COUNTER 5.1 will probably have new types
    ag_type_map: dict[str, str] = {
        "Article": "Periodicals",
        "Book_Segment": "eBooks",
        "Book": "eBooks",
        "Database": "Other",
        "Journal": "Periodicals",
        "Multimedia": "Multimedia",
        "Newspaper_or_Newsletter": "Periodicals",
        "Other": "Other",
        "Platform": "Other",
        "Report": "Other",
        "Thesis_or_Dissertation": "eBooks",
    }
    for dtype in data["Resource Types"].keys():
        if not ag_type_map.get(dtype, False):
            print(
                "Data type '{}' is not categorized under our aggregated types anywhere, ignoring this data.".format(
                    dtype
                )
            )
        else:
            data["Aggregated Resource Types"][ag_type_map[dtype]] += data[
                "Resource Types"
            ][dtype].get("Total_Item_Requests", 0)
            data["Aggregated Resource Types"]["Total"] += data["Resource Types"][
                dtype
            ].get("Total_Item_Requests", 0)


def main(root_path: Path) -> None:
    # parse year from end of path
    try:
        year: int | None = int(str(root_path).split(os.sep).pop())
    except ValueError:
        year = None

    for root, dirs, files in os.walk(root_path):
        for name in files:
            if name.endswith("_PR.json"):
                print("Processing report {}".format(name))
                with open(Path(root) / name, "r") as fh:
                    report: dict[str, Any] = json.load(fh)
                    report_version: str = report["Report_Header"]["Release"]
                    counter_parsers[report_version](report)

    calc_aggregated(data)
    filename: str = f"{year}-counts.json" if year else "counts.json"
    with open(filename, "w") as fh:
        json.dump(data, fh, indent=2, sort_keys=True)
        print("Finished. Wrote results to {}".format(filename))


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Aggregate usage statistics from COUNTER 5 Platform Reports downloaded in bulk via the COUNTER 5 Report Tool."
    )
    parser.add_argument(
        "path",
        metavar="path/to/year",
        type=Path,
        nargs=1,
        help="path to the year of JSON reports, e.g. .DO_NOT_MODIFY/_json/2024",
    )
    args: argparse.Namespace = parser.parse_args()
    main(args.path[0])
