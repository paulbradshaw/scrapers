#!/usr/bin/env python

#start at http://www.audit-scotland.gov.uk/performance/council/ for 09/10-11/12
#first sheet is 'Corporate Management & Benefits'
#Each year can be accessed as follows, from 2001 to this:
#'http://www.audit-scotland.gov.uk/performance/council/index.php?year=2011'
#files end in xls

import scraperwiki
import requests
import lxml.html
import xlrd
import urlparse
import urllib
import random

#function to scrape the first sheet of excel file
def scrape_xls(xls):
    xlbin = scraperwiki.scrape(xls)
    book = xlrd.open_workbook(file_contents=xlbin)
    #loop through each sheet
    for sheet in book.sheets():
        #print the sheet's name, rows and cols
        print "Sheet called %s has %s rows and %s columns" %(sheet.name,sheet.nrows,sheet.ncols)
        #put first row in 'title'
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
#WE DON"T KNOW HOW MANY rows THERE ARE IN EACH SHEET?, so we create a range to cycle through:
        for i in range(4,sheet.nrows):
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
                scraperwiki.sql.save(['url','measure','year','category'],record)
    
#START HERE: function to find the excel links
def find_xls(url):
    html = scraperwiki.scrape(url)
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

#START here: loop through a range of years...
for year in range(2001,2013):
    yearurl = 'http://www.audit-scotland.gov.uk/performance/council/index.php?year='+str(year)
    print "SCRAPING: ", yearurl
    find_xls(yearurl)
