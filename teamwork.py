#!/usr/bin/env python3
import argparse
import csv
from datetime import datetime

# map to convert Teamwork "Agent" name into CCA email
name_email_map: dict[str, str] = {
    "Adrian Applin": "adrian",
    "Alia Moussa": "aliamoussa",
    "Amber Bales": "abales",
    "Annemarie Haar": "ahaar",
    "Bobby Deetz": "bobbydeetz",
    "Bobby White": "bobbywhite",
    "Daniel Ransom": "dransom",
    "Eric Phetteplace": "ephetteplace",
    "Lisa Conrad": "lconrad",
    "Mingyu Li": "mingyuli",
    "Nancy Chan": "nchan",
    "Rubi Sanmiguel": "rsanmiguel",
    "Ryan Segal": "ryansegal",
    "Sunny Satpathy": "santrupti.satpathy",
    "Teri Dowling": "tdowling",
}


def parse_argument() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="calculate Teamwork stats for Libraries team"
    )
    parser.add_argument("file", nargs=1, type=str, help="CSV input file from Teamwork")
    parser.add_argument(
        "--out",
        required=False,
        default="refstats.csv",
        help="output file (default: refstats.csv)",
    )
    parser.add_argument(
        "--everyone", action="store_true", help="include non-Libraries staff in output"
    )
    return parser.parse_args()


def process_tags(tags) -> dict[str, str]:
    """Look in Teamwork Desk "Tags" for info that fits into our other categories

    Args: tags string
    Returns: dict with patron_type, location, and details properties
    """
    # hash breaking out particular fields we can find in Teamwork tags
    d = {
        "patron_type": "",
        "location": "Online",
        "details_list": set(),
        "details": "",
    }
    for tag in tags.split(","):
        # ! For patron type, if there are multiple matching TWD tags then the
        # ! first match is used, e.g. "Staff,Faculty" -> patron type = "Staff"
        ptypes = [
            "Undergrad",
            "Faculty",
            "Grad Student",
            "Staff",
            "Alumni",
            "Pre-college",
        ]
        for type in ptypes:
            if type.lower() in tag.lower():
                d["patron_type"] = type
                break

        # tickets often tagged merely "student", we assume most are undergrads
        if "student" in tag.lower() and d["patron_type"] == "":
            d["patron_type"] = "Undergrad"

        if "san francisco" in tag.lower():
            d["location"] = "San Francisco"

        # look for tags similar to any of our "Details" options
        details = [
            "Archives Consultation",
            "Digital Scholarship",
            "Materials Library",
            "Moodle",
            "MURAL",
            "Panopto",
            "Portal",
            "Printing",
            "VAULT",
            "VoiceThread",
            "Zoom",
        ]
        for detail in details:
            if detail.lower() in tag.lower():
                d["details_list"].add(detail)

        if "google" in tag.lower():
            d["details_list"].add("Google Apps for Education")

    # construct comma-separated details string from python set
    d["details"] = ", ".join(d["details_list"])
    return d


def convert(tw) -> list[str]:
    """Convert Teamwork Desk statistics into our Reference Statistics

    Args:
        teamwork: dict of CSV row from Teamwork Desk output
        Teamwork CSV fields (in order): ID,URL,Subject,Inbox,Status,Type,Source,Priority,Tagged,Agent,Customer,
        Email,Company,TimeTracked,TimeBilled,CreatedAt,UpdatedAt

    Returns:
        refstats: list of CSV row in refstats google sheet format
        Refstats fields: Date/Time,Email Address,Type,Mode of Communication,Patron Type,Details,Notes,Location
    """
    rs = []

    # Teamwork Desk date format has changed multiple times, common break point
    # Currently looks like 2022-10-22 07:38:08 -0700 PDT
    datecreated = datetime.strptime(tw["CreatedAt"], "%Y-%m-%d %H:%M:%S %z %Z")

    rs.append(datecreated.strftime("%m/%d/%Y %H:%M:%S"))
    # map names to emails, note exceptions
    if tw["Agent"] in name_email_map:
        rs.append(name_email_map[tw["Agent"]] + "@cca.edu")
    elif args.everyone:
        rs.append(tw["Agent"])
    else:
        print('"{}" not in the name->email mapping, exiting'.format(tw["Agent"]))
        exit(1)
    # options are Directional, Reference, Service, Technical/Computing (best fit)
    rs.append("Technical/Computing")
    mode = tw["Source"].replace(" (Manual)", "").replace("Docs", "Email")
    rs.append(mode)
    tags = process_tags(tw["Tagged"])
    rs.append(tags["patron_type"])
    rs.append(tags["details"])
    rs.append(f"https://projects.cca.edu/desk/tickets/{tw['ID']}")
    rs.append(tags["location"])

    return rs


def parse_file(file):
    with open(file, "r") as infile:
        with open(args.out, "w") as outfile:
            reader = csv.DictReader(infile)
            writer = csv.writer(outfile)
            # write header row
            writer.writerow(
                [
                    "Date/Time",
                    "Email Address",
                    "Type",
                    "Mode of Communication",
                    "Patron Type",
                    "Details",
                    "Notes",
                    "Location",
                ]
            )
            for row in reader:
                if args.everyone or row["Agent"] in name_email_map:
                    writer.writerow(convert(row))


if __name__ == "__main__":
    global args
    args = parse_argument()
    parse_file(args.file[0])
