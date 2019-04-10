#!/usr/bin/env python


import scraperwiki
import urlparse
import lxml.html
import urllib2

#For testing
testurl = "https://sheffield.citizenspace.com/"
aggurl = "https://aggregator.delib.net/citizenspace/?state_filter=closed&search_text=&region=&source=&custom_sort=newest_update&per_page=500&page=033"
closedconsultations = "consultation_finder/?sort_on=iconsultable_enddate&sort_order=descending&advanced=1&st=closed#cs-finder-results-container"
#Change this when doing other urls
url = testurl+closedconsultations
print "scraping %s" % url




