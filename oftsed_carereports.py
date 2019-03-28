#!/usr/bin/env python


import scraperwiki
import urlparse
import lxml.html
import urllib2
import requests

#Here are URLs from the 3 levels we want to scrape:
#This first one allows you to get all results on one page by changing the rows= parameter
resultsurl = "https://reports.ofsted.gov.uk/search?q=&location=&lat=&lon=&radius=&level_1_types=3&level_2_types%5B0%5D=12&start=0&status%5B0%5D=1&rows=170"
councilurl = "https://reports.ofsted.gov.uk/provider/44/80429"
pdfurl = "https://files.api.ofsted.gov.uk/v1/file/50050254"

#Define a function to scrape all the links to each council's page
def grabcouncillinks(url):
    html = requests.get(url, verify=False)
    root = lxml.html.fromstring(html.content)
    #Grab all the <span class="pn"> to find out which is the biggest page number inside those
    listlinks = root.cssselect('li h3 a')
    print(len(listlinks))
    record = {}
    for link in listlinks[:3]:
        #print(link.text_content())
        #print(link.attrib['href'])
        fullurl = "https://reports.ofsted.gov.uk"+link.attrib['href']
        record['authority'] = link.text_content()
        record['code'] = link.attrib['href'].split("/")[-1]
        record['url'] = fullurl
        print(record)
        scraperwiki.sqlite.save(['url'], record, table_name = 'councilurls')
        scrapecouncilpage(fullurl)

#Define a function to scrape a council page
def scrapecouncilpage(url):
    print("scraping",url)
    #we want links like this: <a class="publication-link" target="_blank" href="https://files.api.ofsted.gov.uk/v1/file/2753832">
    #Containing text: Children&#039;s services inspection  
    html = requests.get(url, verify=False)
    root = lxml.html.fromstring(html.content)
    listlinks = root.xpath("//a[contains(text(),'s services inspection')]")
    print(len(listlinks))
    print(len(reportlinks))
    print(listlinks[0].text_content())
    print(listlinks[0].attrib['href'])
    #UNFINISHED

grabcouncillinks(resultsurl)
