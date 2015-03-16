#!/usr/bin/env python

#start at http://www.audit-scotland.gov.uk/performance/council/ for 09/10-11/12
#first sheet is 'Corporate Management & Benefits'
#Each year can be accessed as follows, from 2001 to this:
#'http://www.audit-scotland.gov.uk/performance/council/index.php?year=2011'
#files end in xls

#PROBLEM: Year pages 2001-2007 have PDF, not Excel. 2008 files do show 2006/07 figures
#PROBLEM: Sheet 1 is not always Corporate Management, or consistently named

import scraperwiki
import requests
import lxml.html
import xlrd
import urlparse
import urllib
import random

#SECOND function to scrape the first sheet of excel file passed to it
def scrape_xls(xls):
    #scrape into 'xlbin' variable
    xlbin = scraperwiki.scrape(xls)
    #put into xlrd object 'book'
    book = xlrd.open_workbook(file_contents=xlbin)
    #put first sheet into variable 'sheet'
    sheet = book.sheet_by_index(0)
    #put first row into 'title'
    title = sheet.row_values(0)
    #print the first cell of that row
    print "First row, first cell", title[0]
    #put the 5th column in 'keys'
    keys = sheet.col_values(4)
    #print the first cell in that column
    print "5th column, first cell", keys[0]
    #create an empty record
    record = {}
    #we need the following fields: authority, sheetname, measure, year, value
    #put the first cell in the first row (title) in 'authority'
    authority = title[0]
    #put the 5th cell in the first row (title) in 'sheetname'
    sheetname = title[4]
    print "sheetname", sheetname
    #there are 44 rows, starting in row 5, so we create a range to cycle through:
    for i in range(4,48):
        print i
        measure = sheet.col_values(4)[i]
        print measure
        #There are 3 year columns, so we loop through those indexes
        for col in range(5,8):
            year = title[col]
            value = sheet.col_values(col)[i]
            print "year and value:", year, value
            record['authority'] = authority
            record['category'] = sheetname
            record['measure'] = measure
            record['year'] = year
            record['value'] = value
            record['url'] = xls
            #idno = idno+1
            #record['id'] = idno
            record['primarykey'] = authority+":"+measure+":"+year
            #unique_keys = ['primarykey']
            record['randomno'] = random.randint(0,1000000000)
            print "---", record
            scraperwiki.sql.save(['url','measure','year'],record)
    
#FIRST function: finds the excel links in any page sent to it
def find_xls(url):
    #scrape into variable 'html'
    html = scraperwiki.scrape(url)
    #convert from string object to lxml object 'root'
    root = lxml.html.fromstring(html)
    #grab all links within <li class="excel"><a ...>
    links = root.cssselect('li.excel a')
    for xls in links:
        #for each one: show the href= attribute
        print "XLS", xls.attrib['href']
        concaturl = 'http://www.audit-scotland.gov.uk/performance'+xls.attrib['href'].replace("..","")
        #urlparse returns the wrong URL here, stripping out the 'performance' folder
        parsedurl = urlparse.urljoin('http://www.audit-scotland.gov.uk/performance/', xls.attrib['href'])
        print "parsedurl", parsedurl
        print "concatenated URL", concaturl
        #run the scrape_xls function on that url
        scrape_xls(concaturl)

#START here. Each URL ends in the accounting year end
#so we loop through those years...
for year in range(2001,2012):
    #...and add to the URL
    yearurl = 'http://www.audit-scotland.gov.uk/performance/council/index.php?year='+str(year)
    print "SCRAPING", yearurl
    #then run the find_xls function (defined above) on that url
    find_xls(yearurl)
