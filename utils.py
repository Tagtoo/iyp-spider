#!/usr/bin/env python

import urlparse
import urllib
import urllib2
from multiprocessing.dummy import Pool as ThreadPool

# Sample data
SAMPLE_LASTPAGE_LINK = "http://www.iyp.com.tw/showroom.php?cate_name_eng_lv1=financial&cate_name_eng_lv3=credit-unions&p=33"

def range_all_links(sampleLinks):
    result = map(range_all_page_links, sampleLinks)
    # flatten the result
    return [item for sublist in result for item in sublist]

def range_all_page_links(lastPageUrl):
    """
    for url sample please refer to SAMPLE_LASTPAGE_LINK
    argument: a sample url with the last one p parameter
    return: a list of all page links by replace the p parameter
    """
    # function: to replace the p query parameter to new p
    def get_link_with_p(urlParse, p):
        scheme, netloc, path, query, fragment = urlParse
        newQueryDict = urlparse.parse_qs(query)
        newQueryDict['p'] = p
        newQuery = urllib.urlencode(newQueryDict, True)

        return urlparse.urlunsplit((scheme, netloc, path, newQuery, fragment))

    urlParseResult = urlparse.urlsplit(lastPageUrl)
    queryParseResult = urlparse.parse_qs(urlParseResult.query)
    result = []
    
    # determine the page range: 33 -> 0...33
    endPageNumber = int(queryParseResult['p'][0])
    pageRange = range(endPageNumber+1)

    for p in pageRange:
        result.append(get_link_with_p(urlParseResult, p))

    return result


def urlfetch_all_links(links):
    """
    Fetch all webpages.
    argument: links :: [ link::String ]
    return: [ pageContent::String ]
    """
    def http_fetch_content(url):
        opener = urllib2.urlopen(url)
        return opener.read()
    pool = ThreadPool(20)
    results = pool.map(http_fetch_content, links)
    pool.close()
    pool.join()

    return results

    
if __name__ == '__main__':
    import pprint

    # get all links
    links = range_all_page_links(SAMPLE_LASTPAGE_LINK)
    pprint.pprint(links)

    # fetch all link content
    contentList = urlfetch_all_links(links)
    pprint.pprint(contentList[0:1])

    

