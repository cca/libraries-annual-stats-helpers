#!/usr/bin/env python3
"""
Summarize a year's worth of COUNTER usage statistics.
The data is stored in the COUNTER 5 Reports Tool app's "all_data" folder
which this script expects to exist in an "all_data" directory under your user's
home. You must run that tool before summarizing the reports.
"""
import argparse
import json
import os

data = {
    "Platforms": {},
    "Resource Types": {},
    "Aggregated Resource Types": {
        "eBooks": 0,
        "Multimedia": 0,
        "Other": 0,
        "Periodicals": 0,
    }
}


def add_or_init(platform, dtype, metric, count):
    """ Add to an existing category in the data dict
    or initialize one if it does not already exist.

    Args:
        platform (str): vendor platform, e.g. "ProQuest"
        dtype (str): data type from COUNTER report, e.g. "Book"
        metric (str): usage type from COUNTER report, e.g. "Unique_Item_Requests"
        count (int): count of usage metric, e.g. 23
    """
    global data

    # case 1: platform does not yet exist
    if not data["Platforms"].get(platform, False):
        data["Platforms"][platform] = { metric: count }
    # case 2: we have the platform but not this particular metric
    elif not data["Platforms"][platform].get(metric, False):
        data["Platforms"][platform][metric] = count
    # case 3: we have both & just need to add to the total
    else:
        data["Platforms"][platform][metric] += count

    if not data["Resource Types"].get(dtype, False):
        data["Resource Types"][dtype] = { metric: count }
    elif not data["Resource Types"][dtype].get(metric, False):
        data["Resource Types"][dtype][metric] = count
    else:
        data["Resource Types"][dtype][metric] += count


def calc_aggregated(data):
    """ Combine media categories to receive an aggregated total

    Args:
        data (dict): data object populated from COUNTER reports (see top of this file)

    2023 IPEDS guidance: different platform types use different metrics for their totals.
    - Ebooks: BR_T1 use unique title request
    - Multimedia: IR_M1 use total item request
    - E-serial: TR_J1 use unique title request

    For now we are just using total item requests across the board but putting this here for future reference.
    """
    ag_type_map = {
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
            print("Data type '{}' is not categorized under our aggregated types anywhere, ignoring this data.".format(dtype))
        else:
            data["Aggregated Resource Types"][ag_type_map[dtype]] += data["Resource Types"][dtype].get("Total_Item_Requests", 0)


def main(year):
    for root, dirs, files in os.walk("{}/all_data/.DO_NOT_MODIFY/_json/{}".format(os.path.expanduser('~'), year)):
        for name in files:
            if name.endswith("_PR.json"):
                print("Processing report {}".format(name))
                with open(os.path.join(root, name), 'r') as fh:
                    report = json.load(fh)
                    for item in report.get("Report_Items", []):
                        dtype = item["Data_Type"]
                        platform = item["Platform"]
                        for period in item["Performance"]:
                            for instance in period["Instance"]:
                                metric = instance["Metric_Type"]
                                count = instance["Count"]
                                # print("{} {} for type {} on {}".format(count, metric, dtype, platform))
                                add_or_init(platform, dtype, metric, count)

    calc_aggregated(data)
    filename = "{}-counts.json".format(year)
    with open(filename, 'w') as fh:
        json.dump(data, fh, indent=2, sort_keys=True)
        print("Finished. Wrote results to {}".format(filename))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Aggregate usage statistics from COUNTER 5 Platform Reports downloaded in bulk via the COUNTER 5 Report Tool.')
    parser.add_argument('year', metavar='YYYY', type=int, nargs=1, help='calendar year to compile stats for')
    args = parser.parse_args()
    main(args.year[0])
