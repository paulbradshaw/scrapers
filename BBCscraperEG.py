#!/usr/bin/env python

import scraperwiki
import requests
import lxml.html

bbcurl = "http://www.bbc.co.uk/news/england/birmingham_and_black_country/"

html = scraperwiki.scrape(bbcurl)
print lxml.html.fromstring(html)
root = lxml.html.fromstring(html)
h2s = root.cssselect('a.story')
print h2s
record = {}
listofterms = ['crime','murder']
for headline in h2s:
    h2 = headline.text_content()
    headlineurl = headline.attrib.get('href')
    print headlineurl
    for term in listofterms:
        if term in h2:
            print "YAHHEE"
            print h2
            record['newstitle'] = h2
            record['url'] = bbcurl
            print record
            scraperwiki.sql.save(['newstitle'],record)
    
