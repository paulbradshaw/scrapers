#!/usr/bin/env python
#Import our libraries that we need to grab the URLs and scrape them
import scraperwiki
import requests
import urllib2
import lxml.html

baseurl = "http://democracy.towerhamlets.gov.uk/"
councillorsurl = "http://democracy.towerhamlets.gov.uk/mgMemberIndex.aspx?bcr=1"

record ={}

#Set headers for scrapers
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
timeout=0.25
print 'scraping', councillorsurl
req = urllib2.Request(councillorsurl, None, headers)
doc = lxml.html.parse(urllib2.urlopen(req))
links = doc.xpath('//li/a')
councillorlinks = []
for link in links:
    linkhref = link.attrib['href']
    if linkhref[0:10] == "mgUserInfo":
        councillorlinks.append(linkhref)
    else:
        print linkhref
    #print councillorlinks
for link in councillorlinks[7:]:
    fullurl = baseurl+link
    print 'scraping', fullurl
    req = urllib2.Request(fullurl, None, headers)
    doc = lxml.html.parse(urllib2.urlopen(req))
    infolinks = doc.xpath('//ul[1]/li/a')
    print len(infolinks)
    print infolinks[20].text_content()
    print infolinks[20].attrib['href']
    for link in infolinks:
        #If it is a Register of Interest link...
        if "mgRofI.aspx" in link.attrib['href']:
            reglink = link.attrib['href']
            fullreglink = baseurl+reglink
            print 'scraping', fullreglink
            req = urllib2.Request(fullreglink, None, headers)
            doc = lxml.html.parse(urllib2.urlopen(req))
            h2s = doc.xpath('//h2')
            councillorname = h2s[0].text_content()
            record['councillorname'] = councillorname
            lis = doc.xpath('//ul[@class="mgActionList"]/li')
            pubdate = lis[0].text_content().replace('This register of interests was published on ','')
            record['pubdate'] = pubdate
            #Now the cssselect option
            html = scraperwiki.scrape(fullreglink)
            #print html
            root = lxml.html.fromstring(html)
            #Grab all tables with this class - xpath option would be
            #tables = doc.xpath('//table[@class="mgInterestsTable"]')
            tablescss = root.cssselect('table.mgInterestsTable')
            print 'tables counted', len(tablescss)
            if len(tablescss)>4:
                #The 6th table is tenancies, grab all cells
                tenancytable = tablescss[5].cssselect('tr td')
                #The first cell is 'Yourself'
                tenanciesself = tenancytable[0].text_content()
                tenanciesother = tenancytable[1].text_content()
                print 'tenancy', tenanciesself
                record['tenanciesself'] = tenanciesself
                record['tenanciesother'] = tenanciesother
                record['url'] = fullreglink
                scraperwiki.sql.save(['url'],record,table_name="registertowerhamlets")
            else:
                record['tenanciesself'] = "NOT SCRAPED"
                record['tenanciesother'] = "NOT SCRAPED"
                record['url'] = fullreglink
                scraperwiki.sql.save(['url'],record,table_name="registertowerhamlets")
