#!/usr/bin/env python

from utils import *
from parse import *

import drive

import pprint
import csv
import uuid
import os

OUTPUT_DIRECTORY = "output"
OUTPUT_CSV_FILENAME = 'output/output.csv'
SAMPLE_CATEGORY_LINKS = "samples/category_urls.txt"
UPLOAD_FILENAME = "yellowpage-" + str(uuid.uuid4())

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

def to_csv(data):
    order = ('uid', 'title', 'phone', 'address')

    os.mkdir(OUTPUT_DIRECTORY)
    filename = OUTPUT_CSV_FILENAME

    with open(filename, 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, order)
        for item in data:
            writer.writerow(dict_encode_utf8(item))

    return filename

def main():
    categoryLinks = get_category_links(SAMPLE_CATEGORY_LINKS)
    allLinks = range_all_links(categoryLinks)

    allPageContent = urlfetch_all_links(allLinks)
    allItems = map(get_data, allPageContent)
    allItems = [ item for sublist in allItems for item in sublist ] #flatten

    outputFile = to_csv(allItems)
    print "output: " + outputFile

    drive.put_csv(outputFile, UPLOAD_FILENAME)
    

if __name__ == '__main__':
    main()

