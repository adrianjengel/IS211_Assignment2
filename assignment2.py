#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""IS211 Assignment2. Working with different modules."""

import urllib2
import csv
import datetime
import logging
import argparse
import sys


def main():
    """A function that fetches a CSV file and stores the data in a dict."""

    def downloadData(url):
        """Fetch the CSV file."""
        get_url = urllib2.urlopen(url)
        return get_url

    def processData(data):
        """Process the CSV file and store in a dictionary."""
        csv_file = csv.reader(data)
        persondict = {}
        csv_file.next()

        for row in csv_file:
            try:
                row[2] = datetime.datetime.strptime(row[2], "%d/%m/%Y")
            except ValueError:
                id_num = int(row[0])
                line = int(row[0])+1
                logger = logging.getLogger(" assignment2")
                logger.error(" Error processing line #{} for ID #{}.".format(line, id_num))

            persondict[int(row[0])] = (row[1], row[2])
        return persondict

    def displayPerson(id, personData):
        """Display a person's info."""
        try:
            response = "Person #{idnum} is {name} with a birthday of {date}"
            print response.format(idnum=id, name=personData[id][0], date=personData[id][1])
        except KeyError:
            print "No person found with that ID #."

    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="The URL to fetch a CSV file.")
    args = parser.parse_args()
    logging.basicConfig(filename="errors.log", level=logging.ERROR)

    if args.url:
        csvData = downloadData(args.url)
        personData = processData(csvData)
        msg = "Please enter an ID #. Enter 0 or a negative # to exit. "

        while True:
            try:
                user = int(raw_input(msg))
            except ValueError:
                print "Invalid input. Please try again."
                continue
            if user > 0:
                displayPerson(user, personData)
            else:
                print "Thank you."
                sys.exit()
    else:
        print "Please use the --url parameter."

if __name__ == "__main__":
    main()
