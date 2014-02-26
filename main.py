#!/usr/bin/env python

from utils import *
from parse import *
import apiclient

import drive

import pprint
import csv
import uuid
import os
import sys

SAMPLE_CATEGORY_LINKS = "samples/category_urls.txt"
OUTPUT_DIRECTORY = "output"

def dict_encode_utf8(d):
    for key in d:
        d[key] = d[key].encode('utf-8')
    return d

def get_category_links(filename):
    """
    get category links from a file
    """
    content = open(filename).read().strip()
    links = content.split()
    return links

def to_csv(data, filename):
    order = ('uid', 'title', 'phone', 'address')

    try:
        os.makedirs(OUTPUT_DIRECTORY)
    except OSError as ose:
        print 'mkdir: %s' % ose

    with open(filename, 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, order)
        for item in data:
            writer.writerow(dict_encode_utf8(item))

    return filename

def fetch_a_category(filename):
    CATEGORY_NAME = filename.split("/")[-1].replace(".txt", "")
    UUID = str(uuid.uuid4()).split("-")[-1]
    UPLOAD_FILENAME = "yellowpage-%s-%s" % (CATEGORY_NAME, UUID)
    OUTPUT_CSV_FILENAME = '%s/output-%s-%s.csv' % (OUTPUT_DIRECTORY, CATEGORY_NAME, UUID)

    categoryLinks = get_category_links(filename)
    allLinks = range_all_links(categoryLinks)

    allPageContent = urlfetch_all_links(allLinks)
    allItems = map(get_data, allPageContent)
    allItems = [ item for sublist in allItems for item in sublist ] #flatten

    to_csv(allItems, OUTPUT_CSV_FILENAME)
    print "output: " + OUTPUT_CSV_FILENAME

    try:
        drive.put_csv(OUTPUT_CSV_FILENAME, UPLOAD_FILENAME)
    except apiclient.errors.HttpError as her:
        print her

def main():
    if len(sys.argv) < 2:
        print "please specify the input files."
    else:
        files = sys.argv[1:]
        for fileName in files:
            print "fetching %s..." % fileName
            fetch_a_category(fileName)

if __name__ == '__main__':
    main()

