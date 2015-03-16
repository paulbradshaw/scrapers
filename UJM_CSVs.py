#!/usr/bin/env python
# -*- coding: latin-1 -*-

import scraperwiki
import csv
import requests
import lxml.html

baseurl = "ftp://ftp.zois.co.uk/pub/jcp/"
csvlist = ['UJM-scrape-2013-09-01.csv','UJM-scrape-2013-09-02.csv']
#,'UJM-scrape-2013-09-03.csv','UJM-scrape-2013-09-04.csv','UJM-scrape-2013-09-05.csv','UJM-scrape-2013-09-06.csv','UJM-scrape-2013-09-07.csv','UJM-scrape-2013-09-08.csv','UJM-scrape-2013-09-09.csv','UJM-scrape-2013-09-10.csv','UJM-scrape-2013-09-11.csv','UJM-scrape-2013-09-12.csv','UJM-scrape-2013-09-13.csv','UJM-scrape-2013-09-14.csv','UJM-scrape-2013-09-15.csv','UJM-scrape-2013-09-16.csv','UJM-scrape-2013-09-17.csv','UJM-scrape-2013-09-18.csv','UJM-scrape-2013-09-19.csv','UJM-scrape-2013-09-20.csv','UJM-scrape-2013-09-21.csv','UJM-scrape-2013-09-22.csv','UJM-scrape-2013-09-23.csv','UJM-scrape-2013-09-24.csv','UJM-scrape-2013-09-25.csv','UJM-scrape-2013-09-26.csv','UJM-scrape-2013-09-27.csv','UJM-scrape-2013-09-28.csv','UJM-scrape-2013-09-29.csv','UJM-scrape-2013-09-30.csv','UJM-scrape-2013-10-01.csv','UJM-scrape-2013-10-02.csv','UJM-scrape-2013-10-03.csv','UJM-scrape-2013-10-04.csv','UJM-scrape-2013-10-05.csv','UJM-scrape-2013-10-06.csv','UJM-scrape-2013-10-07.csv','UJM-scrape-2013-10-08.csv','UJM-scrape-2013-10-09.csv','UJM-scrape-2013-10-10.csv','UJM-scrape-2013-10-11.csv','UJM-scrape-2013-10-12.csv','UJM-scrape-2013-10-13.csv','UJM-scrape-2013-10-14.csv','UJM-scrape-2013-10-15.csv','UJM-scrape-2013-10-16.csv','UJM-scrape-2013-10-17.csv','UJM-scrape-2013-10-18.csv','UJM-scrape-2013-10-19.csv','UJM-scrape-2013-10-20.csv','UJM-scrape-2013-10-21.csv','UJM-scrape-2013-10-22.csv','UJM-scrape-2013-10-23.csv','UJM-scrape-2013-10-24.csv','UJM-scrape-2013-10-25.csv','UJM-scrape-2013-10-26.csv','UJM-scrape-2013-10-27.csv','UJM-scrape-2013-10-28.csv','UJM-scrape-2013-10-29.csv','UJM-scrape-2013-10-30.csv','UJM-scrape-2013-10-31.csv','UJM-scrape-2013-11-01.csv','UJM-scrape-2013-11-02.csv','UJM-scrape-2013-11-03.csv','UJM-scrape-2013-11-04.csv','UJM-scrape-2013-11-05.csv','UJM-scrape-2013-11-06.csv','UJM-scrape-2013-11-07.csv','UJM-scrape-2013-11-08.csv','UJM-scrape-2013-11-09.csv','UJM-scrape-2013-11-10.csv','UJM-scrape-2013-11-11.csv','UJM-scrape-2013-11-12.csv','UJM-scrape-2013-11-13.csv','UJM-scrape-2013-11-14.csv','UJM-scrape-2013-11-15.csv','UJM-scrape-2013-11-16.csv','UJM-scrape-2013-11-17.csv','UJM-scrape-2013-11-18.csv','UJM-scrape-2013-11-19.csv','UJM-scrape-2013-11-20.csv','UJM-scrape-2013-11-21.csv','UJM-scrape-2013-11-22.csv','UJM-scrape-2013-11-23.csv','UJM-scrape-2013-11-24.csv','UJM-scrape-2013-11-25.csv','UJM-scrape-2013-11-26.csv','UJM-scrape-2013-11-27.csv','UJM-scrape-2013-11-28.csv','UJM-scrape-2013-11-29.csv','UJM-scrape-2013-11-30.csv','UJM-scrape-2013-12-01.csv','UJM-scrape-2013-12-02.csv','UJM-scrape-2013-12-03.csv','UJM-scrape-2013-12-04.csv','UJM-scrape-2013-12-05.csv','UJM-scrape-2013-12-06.csv','UJM-scrape-2013-12-07.csv','UJM-scrape-2013-12-08.csv','UJM-scrape-2013-12-09.csv','UJM-scrape-2013-12-10.csv','UJM-scrape-2013-12-11.csv','UJM-scrape-2013-12-12.csv','UJM-scrape-2013-12-13.csv','UJM-scrape-2013-12-14.csv','UJM-scrape-2013-12-15.csv','UJM-scrape-2013-12-16.csv','UJM-scrape-2013-12-17.csv','UJM-scrape-2013-12-18.csv','UJM-scrape-2013-12-19.csv','UJM-scrape-2013-12-20.csv','UJM-scrape-2013-12-21.csv','UJM-scrape-2013-12-22.csv','UJM-scrape-2013-12-23.csv','UJM-scrape-2013-12-24.csv','UJM-scrape-2013-12-25.csv','UJM-scrape-2013-12-26.csv','UJM-scrape-2013-12-27.csv','UJM-scrape-2013-12-28.csv','UJM-scrape-2013-12-29.csv','UJM-scrape-2013-12-30.csv','UJM-scrape-2013-12-31.csv','UJM-scrape-2014-01-01.csv','UJM-scrape-2014-01-02.csv','UJM-scrape-2014-01-03.csv','UJM-scrape-2014-01-04.csv','UJM-scrape-2014-01-05.csv','UJM-scrape-2014-01-06.csv','UJM-scrape-2014-01-07.csv','UJM-scrape-2014-01-08.csv','UJM-scrape-2014-01-09.csv','UJM-scrape-2014-01-10.csv','UJM-scrape-2014-01-11.csv','UJM-scrape-2014-01-12.csv','UJM-scrape-2014-01-13.csv','UJM-scrape-2014-01-14.csv','UJM-scrape-2014-01-15.csv','UJM-scrape-2014-01-16.csv','UJM-scrape-2014-01-17.csv','UJM-scrape-2014-01-18.csv','UJM-scrape-2014-01-19.csv','UJM-scrape-2014-01-20.csv','UJM-scrape-2014-01-21.csv','UJM-scrape-2014-01-22.csv','UJM-scrape-2014-01-23.csv','UJM-scrape-2014-01-24.csv','UJM-scrape-2014-01-25.csv','UJM-scrape-2014-01-26.csv','UJM-scrape-2014-01-27.csv','UJM-scrape-2014-01-28.csv','UJM-scrape-2014-01-29.csv','UJM-scrape-2014-01-30.csv','UJM-scrape-2014-01-31.csv','UJM-scrape-2014-02-01.csv','UJM-scrape-2014-02-02.csv','UJM-scrape-2014-02-03.csv','UJM-scrape-2014-02-04.csv','UJM-scrape-2014-02-05.csv','UJM-scrape-2014-02-06.csv','UJM-scrape-2014-02-07.csv','UJM-scrape-2014-02-08.csv','UJM-scrape-2014-02-09.csv','UJM-scrape-2014-02-10.csv','UJM-scrape-2014-02-11.csv','UJM-scrape-2014-02-12.csv','UJM-scrape-2014-02-13.csv','UJM-scrape-2014-02-14.csv','UJM-scrape-2014-02-15.csv','UJM-scrape-2014-02-16.csv','UJM-scrape-2014-02-17.csv','UJM-scrape-2014-02-18.csv','UJM-scrape-2014-02-19.csv','UJM-scrape-2014-02-20.csv','UJM-scrape-2014-02-21.csv','UJM-scrape-2014-02-22.csv','UJM-scrape-2014-02-23.csv','UJM-scrape-2014-02-24.csv','UJM-scrape-2014-02-25.csv','UJM-scrape-2014-02-26.csv','UJM-scrape-2014-02-27.csv','UJM-scrape-2014-02-28.csv','UJM-scrape-2014-03-02.csv','UJM-scrape-2014-03-03.csv','UJM-scrape-2014-03-04.csv','UJM-scrape-2014-03-05.csv','UJM-scrape-2014-03-06.csv','UJM-scrape-2014-03-07.csv','UJM-scrape-2014-03-08.csv','UJM-scrape-2014-03-09.csv','UJM-scrape-2014-03-10.csv','UJM-scrape-2014-03-11.csv','UJM-scrape-2014-03-12.csv','UJM-scrape-2014-03-13.csv','UJM-scrape-2014-03-14.csv','UJM-scrape-2014-03-15.csv','UJM-scrape-2014-03-16.csv','UJM-scrape-2014-03-17.csv','UJM-scrape-2014-03-18.csv','UJM-scrape-2014-03-19.csv','UJM-scrape-2014-03-20.csv','UJM-scrape-2014-03-21.csv','UJM-scrape-2014-03-22.csv','UJM-scrape-2014-03-23.csv','UJM-scrape-2014-03-24.csv','UJM-scrape-2014-03-25.csv','UJM-scrape-2014-03-26.csv','UJM-scrape-2014-03-27.csv','UJM-scrape-2014-03-28.csv','UJM-scrape-2014-03-29.csv','UJM-scrape-2014-03-30.csv','UJM-scrape-2014-03-31.csv','UJM-scrape-2014-04-01.csv','UJM-scrape-2014-04-02.csv','UJM-scrape-2014-04-03.csv','UJM-scrape-2014-04-04.csv','UJM-scrape-2014-04-05.csv','UJM-scrape-2014-04-06.csv']
for link in csvlist:
    fullurl = baseurl+link
    print "scraping:", fullurl
    data = scraperwiki.scrape(fullurl)
    reader = csv.reader(data.splitlines())
    print reader
    record = {}
    for row in reader:
        record['jobid'] = row[0]
        record['title'] = row[1]
        record['location'] = row[2]
        record['salary'] = row[3].replace("Â£","")
        record['career'] = row[4]
        record['company'] = row[5]
        record['industry'] = row[6]
        record['job_type'] = row[7]
        record['education'] = row[8]
        #record['description'] = row[9]
        record['apply'] = row[10]
        record['reference'] = row[11]
        record['contact'] = row[12]
        record['added'] = row[13]
        record['noted'] = row[14]
        print record
        scraperwiki.sql.save(['jobid'],record)
