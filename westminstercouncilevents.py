#!/usr/bin/env python


import scraperwiki
import urlparse
import lxml.html
import urllib2
import datetime

#more on datetime here: https://www.saltycrane.com/blog/2008/06/how-to-get-current-date-and-time-in/
now = datetime.datetime.now()
currentmonth = now.month
currentyear = now.year
currentday = now.day

print str(now)
print "Current month: %d" % currentmonth
print "Current year: %d" % currentyear
print "Current day: %d" % currentday

baseurl = "http://committees.westminster.gov.uk/"
#Note the M=6 part of the URL and DD=2018 - these will need to be updated with the current month/year - also D=26 with day
juneurl = "http://committees.westminster.gov.uk/mgCalendarAgendaView.aspx?MR=0&M=6&DD=2018&CID=0&OT=&C=-1&D=26"
latesturl = "http://committees.westminster.gov.uk/mgCalendarAgendaView.aspx?MR=0&M="+str(currentmonth)+"&DD="+str(currentyear)+"&CID=0&OT=&C=-1&D="+str(currentday)
print latesturl

record = {}
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
timeout=0.25
req = urllib2.Request(latesturl, None, headers)
#adapting some of the code from https://stackoverflow.com/questions/3569152/parsing-html-with-lxml
doc = lxml.html.parse(urllib2.urlopen(req))
print doc
listlinks = doc.xpath('//ul[@class="mgCalendarWeekEventList"]/li/a')
print len(listlinks)
for link in listlinks:
    print link.text_content()
    print link.attrib['href']
    record['event'] = link.text_content()
    record['url'] = baseurl+link.attrib['href']
    record['searchurl'] = latesturl
    scraperwiki.sqlite.save(['url'], record, table_name="westminsterevents")

