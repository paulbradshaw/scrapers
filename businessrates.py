#!/usr/bin/env python

#import the libraries we'll need
import re
import scraperwiki
import urllib2
import lxml.etree
import lxml.html
import requests
from time import sleep


nurseryurl = 'https://www.tax.service.gov.uk/view-my-valuation/list-valuations-advanced?primaryCriteria=SCAT&number=&street=&town=&postCode=&billingAuthority=&specialCategoryCode=085&baRef=&descriptionCode=&from=&to=&startPage=1#search-results'
mostofurl = 'https://www.tax.service.gov.uk/view-my-valuation/list-valuations-advanced?primaryCriteria=SCAT&number=&street=&town=&postCode=&billingAuthority=&baRef=&descriptionCode=&from=&to='
pageparam = '&startPage=1'
codeparam = '&specialCategoryCode=085'
#key parameter is specialCategoryCode=085 - that's the number for day nurseries but we can add or swap for others

#need to add a sleep command http://stackoverflow.com/questions/23013220/max-retries-exceeded-with-url

#tasks
#1. generate page URLs
#2. grab details
#3. save details


# these settings are for when request is used below
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
timeout=0.01
sleeptime = 0.5

#create an empty record to store data
record = {}
#this is to store any urls that generate errors
errorurls = []

'''
#This function scrapes a results page - and then runs another function in the middle
def grablinks(url):
    print 'RUNNING GRABLINKS ON ', url
    html = requests.get(url, verify=False, timeout=timeout, headers=headers) #verify False to avoid the SSL error for security reasons
    #turn url into lxml object
    root = lxml.html.fromstring(html.content)
    #grab any <a class = "propertyCard-link">
    listinglinks = root.cssselect('a.propertyCard-link')
    #cssselect always creates a list, so we need to loop through it
    for link in listinglinks:
        #show the href= attribute
        linkhref = link.attrib['href']
        print linkhref
        #run the scrapepage function (defined below) on this url
        scrapepage(linkhref)
        #helpfully the title of the listing is also an attribute of the link, but not always, so we use 'try'
        try:
            print link.attrib['title']
        #run function to scrape page
        except:
            print 'no title'

'''
#This function scrapes an individual room page
def scrapepage(url):
    print 'RUNNING SCRAPEPAGE'
    #this line is for when we loop through errorsnodups which are already fully formed URLs like https://www.spareroom.co.uk/flatshare/london/stratford/7233100
    #url = url.split('https://www.spareroom.co.uk')[1]
    print 'SCRAPING ', url
    #turn to lxml object
    # I think they're blocking repeated attempts to access, so...
    #try: 
    html = requests.get(url, verify=False, timeout=timeout, headers=headers) #verify False to avoid the SSL error for security reasons
    sleep(sleeptime)
    #print html.text
    #turn url into lxml object
    root = lxml.html.fromstring(html.content)
    tablerows = root.cssselect('table tr')
    for row in tablerows:
        print 'this is a row'
        cells = row.cssselect('td')
        print 'there are ', len(cells), ' cells'
        if len(cells)>0:
            record['address'] = cells[0].text_content()
            #each page has the location and previous rates, so could be grabbed to create geo patterns and history
            record['url'] = cells[0].cssselect('a')[0].attrib['href']
            record['description'] = cells[1].text_content()
            record['total area'] = cells[2].text_content()
            record['price per m'] = cells[3].text_content()
            record['current rateable value'] = cells[4].text_content()
            print 'record: ', record
            scraperwiki.sqlite.save(['address'],record)
        for cell in cells:
            print cell.text_content()

#scraper begins here

#first, create an empty list
resultsurls = []


#use 'range' to generate a range of numbers from 1-575 and then loop through those
#we know there are that many because 14351/25 = just over 574. But needs to scrape the number of results and divide by 25 instead to be adaptable
for num in range(1,576):
    print num
    #because 'num' is a number, we need to convert it to a string while adding it to the url
    numurl = mostofurl+'&startPage='+str(num)+codeparam
    print numurl
    #add it to our list using .append()
    resultsurls.append(numurl)
print resultsurls

for url in resultsurls[2:4]:  
    print 'scraping ', url
    scrapepage(url)




