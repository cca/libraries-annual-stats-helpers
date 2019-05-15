#!/usr/bin/env python3
import csv
import re
import sys

# convert Teamwork "Agent" name into CCA email
name_email_map = {
    'Bobby White': 'bobbywhite',
    'Ryan Segal': 'ryansegal',
    'Sunny Satpathy': 'santrupti.satpathy',
}


def process_tags(tags):
    """ Look in Teamwork Desk "Tags" for info that fits into our other categories

    Args: tags string
    Returns: dict with patron_type, location, and details properties
    """
    # hash breaking out particular fields we can find in Teamwork tags
    d = {
        'patron_type': '',
        'location': '',
        'details_list': [],
        'details': '',
    }
    for tag in tags.split(','):
        # NOTE: for both patron type & location the way I wrote this, if there
        # are _multiple_ tags of either type then the _last one listed_ is the
        # one that's used e.g. tags = "Staff,Faculty" -> patron_tpe = "Faculty"

        # look for patron types
        ptypes = ['Undergrad', 'Faculty', 'Grad Student', 'Staff', 'Alumni', 'Pre-college']
        for type in ptypes:
            if re.match(type, tag, re.IGNORECASE):
                d['patron_type'] = type

        # look for locations
        locations = ['San Francisco', 'Oakland']
        for location in locations:
            if re.match(location, tag, re.IGNORECASE):
                d['location'] = location

        # look for "details"
        details = [ 'Printing', 'Materials Library', 'VAULT',
            'Misguided Phone Call', 'Moodle', 'Archives Consultation',
            'Digital Scholarship', 'Google Apps for Education', 'VoiceThread',
        ]
        for detail in details:
            if re.match(detail, tag, re.IGNORECASE):
                d['details_list'].append(detail)

    # construct comma-separated details string from python list
    d['details'] = ', '.join(d['details_list'])
    return d


def convert(tw):
    """ Convert Teamwork Desk statistics into our Reference Statistics

    Args:
        teamwork: dict of CSV row from Teamwork Desk output
        Teamwork CSV fields (in order): ID,URL,Subject,Inbox,Status,Type,Source,Priority,Tagged,Agent,Customer,
        Email,Company,TimeTracked,TimeBilled,CreatedAt,UpdatedAt

    Returns:
        refstats: list of CSV row in refstats google sheet format
        Refstats fields: Date/Time,Email Address,Type,Mode of Communication,Patron Type,Details,Notes,Location
    """
    rs = []

    rs.append(tw['CreatedAt'])
    rs.append(name_email_map[tw['Agent']] + '@cca.edu')
    # @TODO - Directional/Reference/Service/Technical/Computing
    # probably only ever service or tech/comp
    rs.append('Service')
    mode = tw['Source'].replace(' (Manual)', '')
    rs.append(mode)
    tags = process_tags(tw['Tagged'])
    rs.append(tags['patron_type'])
    rs.append(tags['details'])
    rs.append('from Teamwork Desk')
    # @TODO can we assume "online" for many of these?
    rs.append(tags['location'])

    return rs


with open(sys.argv[1], 'r') as infile:
    with open('refstats.csv', 'w') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.writer(outfile)
        # write header row
        writer.writerow(['Date/Time','Email Address','Type','Mode of Communication','Patron Type','Details','Notes','Location'])
        for row in reader:
            writer.writerow(convert(row))
