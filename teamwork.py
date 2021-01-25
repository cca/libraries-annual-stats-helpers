#!/usr/bin/env python3
import argparse
import csv
import re
import sys

from dateutil import parser, tz

# map to convert Teamwork "Agent" name into CCA email
name_email_map = {
    'Amber Bales': 'abales',
    'Bobby White': 'bobbywhite',
    'Ryan Segal': 'ryansegal',
    'Sunny Satpathy': 'santrupti.satpathy',
    'Daniel Ransom': 'dransom',
    'Eric Phetteplace': 'ephetteplace',
    'Lisa Conrad': 'lconrad',
    'Nancy Chan': 'nchan',
}


def parse_argument():
    parser = argparse.ArgumentParser(description='calculate Teamwork stats for Libraries team')
    parser.add_argument('file', nargs=1, type=str, help='CSV input file from Teamwork')
    parser.add_argument('--out', required=False, help='optional output file')
    return parser.parse_args()


def process_tags(tags):
    """ Look in Teamwork Desk "Tags" for info that fits into our other categories

    Args: tags string
    Returns: dict with patron_type, location, and details properties
    """
    # hash breaking out particular fields we can find in Teamwork tags
    d = {
        'patron_type': '',
        'location': '',
        'details_list': set(),
        'details': '',
    }
    for tag in tags.split(','):
        # NOTE: for both patron type & location the way I wrote this, if there
        # are _multiple_ tags of either type then the _last one listed_ is the
        # one that's used e.g. tags = "Staff,Faculty" -> patron_type = "Faculty"
        ptypes = ['Undergrad', 'Faculty', 'Grad Student', 'Staff', 'Alumni', 'Pre-college']
        for type in ptypes:
            if re.match(type, tag, re.IGNORECASE):
                d['patron_type'] = type

        # tickets often tagged merely "student", we assume most are undergrads
        if re.match('student', tag, re.IGNORECASE):
            d['patron_type'] = 'Undergrad'

        locations = ['San Francisco', 'Oakland']
        for location in locations:
            if re.match(location, tag, re.IGNORECASE):
                d['location'] = location

        # look for tags similar to any of our "Details" options
        details = [ 'Printing', 'Materials Library', 'VAULT',
            'Misguided Phone Call', 'Moodle', 'Archives Consultation',
            'Digital Scholarship', 'Google Apps for Education', 'VoiceThread',
            'Google Classroom',
        ]
        for detail in details:
            if re.match(detail, tag, re.IGNORECASE):
                d['details_list'].add(detail)

        if re.match('google', tag, re.IGNORECASE) and 'Google Classroom' not in d['details_list']:
            d['details_list'].add('Google Apps for Education')

    # if we don't have a location, set it to "Online"
    if d['location'] == '':
        d['location'] = 'Online'
    # construct comma-separated details string from python set
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

    # parse date string & convert to local timezone
    date = parser.parse(tw['CreatedAt']).replace(tzinfo=tz.tzutc()).astimezone(tz.tzlocal())

    rs.append(date)
    # map names to emails, note exceptions
    if tw['Agent'] in name_email_map:
        rs.append(name_email_map[tw['Agent']] + '@cca.edu')
    else:
        print('{} not in the name->email mapping'.format(tw['Agent']))
        rs.append(tw['Agent'])
    # options are Directional, Reference, Service, Technical/Computing (best fit)
    rs.append('Technical/Computing')
    mode = tw['Source'].replace(' (Manual)', '').replace('Docs', 'Email')
    rs.append(mode)
    tags = process_tags(tw['Tagged'])
    rs.append(tags['patron_type'])
    rs.append(tags['details'])
    rs.append('Teamwork Desk')
    rs.append(tags['location'])

    return rs


def parse_file(infile):
    with open(sys.argv[1], 'r') as infile:
        outfile_name = args.out or 'refstats.csv'
        with open(outfile_name, 'w') as outfile:
            reader = csv.DictReader(infile)
            writer = csv.writer(outfile)
            # write header row
            writer.writerow(['Date/Time','Email Address','Type','Mode of Communication','Patron Type','Details','Notes','Location'])
            for row in reader:
                writer.writerow(convert(row))


if __name__ == '__main__':
    args = parse_argument()
    parse_file(args.file)
