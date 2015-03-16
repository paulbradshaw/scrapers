#!/usr/bin/env python

#Base page is: http://www.transfermarkt.co.uk/en/default/startseite/berater.html
#Need to visit each link and scrape list of players etc.

import scraperwiki
import lxml.html

baseurl = 'http://www.transfermarkt.co.uk'
starturl = 'http://www.transfermarkt.co.uk/en/default/startseite/berater.html'
record = {}

def scrape_page(linkurl, agent):
    html = scraperwiki.scrape(linkurl)
    root = lxml.html.fromstring(html)
    rows = root.cssselect("table#spieler tr")
    for row in rows:
        cells = row.cssselect("td a")
        if cells:
            name = cells[1].text_content()
            print "NAME:", name
            print "CLUB?", cells[2].text_content()
            club = cells[2].text_content()
            record['name'] = name
            record['club'] = club
            record['url'] = linkurl
            record['agent'] = agent
            scraperwiki.sqlite.save(['url', 'agent', 'name'], record)
        else:
            print "NO NAME/CLUB?"

def scrape_links(starturl):
    html = scraperwiki.scrape(starturl)
    root = lxml.html.fromstring(html)
    links = root.cssselect("td a")
    #NEED TO GRAB EXTRA INFO AND PASS
    for link in links:
        print link.text_content()
        agent = link.text_content()
        linkurl = link.attrib.get('href')
        scrape_page(baseurl+linkurl, agent)

scrape_links(starturl)

# Saving data:
# unique_keys = [ 'id' ]
# data = { 'id':12, 'name':'violet', 'age':7 }
# scraperwiki.sql.save(unique_keys, data)
