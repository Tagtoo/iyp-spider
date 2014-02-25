#!/usr/bin/env python
"""
Parse Module
"""
import pyquery

SAMPLE_HTML = open("samples/sample.html", 'r').read()

def parse_item(PQ, item):
    """
    Parse the content in a <li>
    """
    def imageLink(s): return "=image(\"%s\")" % s
    
    li = PQ(item)

    # get fields
    uid = item.attrib['id']
    title = li.find("h3").text()
    phoneImgLink = "http:" + li.find("li.tel img")[0].attrib['data-url']
    addressImgLink = "http:" + li.find("li.address img")[0].attrib['data-url']

    return {
            'uid': uid,
            'title': title,
            'phone': imageLink(phoneImgLink),
            'address': imageLink(addressImgLink)
            }

def get_data(html):
    d = pyquery.PyQuery(html)
    # d is now a jQuery $-like function
    items = d("ol > li")

    results = []
    for li in items:
        results.append(parse_item(d, li))
        
    return results

if __name__ == '__main__':
    import pprint
    pprint.pprint(get_data(SAMPLE_HTML))

    

    


    
