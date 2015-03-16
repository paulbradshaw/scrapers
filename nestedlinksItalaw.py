#!/usr/bin/env python

#Question from Todd Tucker here: http://stackoverflow.com/questions/17590783/how-to-scrape-more-than-first-instance-of-triple-nested-list-of-links-in-python

import scraperwiki
import urlparse
import lxml.html
import urllib

def scrape_page(linkurl):
    html = scraperwiki.scrape(linkurl)
    root = lxml.html.fromstring(html)
    title = root.cssselect("h1")
    print "the title:", title[0].text
    record = {}
    record['title'] = title[0].text
    record['url'] = linkurl
    #<div class="field-items"><div class="field-item even"><a
    arbrules = root.cssselect("div.field-items a")
    if arbrules:
        record['arbruleurl'] = arbrules[0].attrib.get("href")
        record['arbrule'] = arbrules[0].text_content()
    else:
        record['arbruleurl'] = "NO URL"
        record['arbrule'] = "NO ARBRULE"
    legalbasis = root.cssselect("div.field-label")
    if legalbasis:
        record['legalbasis'] = legalbasis[0].text_content()
    else:
        record['legalbasis'] = "NO LEGAL BASIS GIVEN"
    extralinks = []
    contents = root.cssselect("div.view-content a")
    if contents:
        for content in contents:
            extralinks.append(content.text_content())
            extralinks.append(content.attrib.get("href"))
        record['extralinks']  = extralinks
    else:
        record['extralinks']  = "NO EXTRA LINKS"
    #record['firstparty'] = title[0].text.split(" v. ")[0]
    #record['secondparty'] = title[0].text.split(" v. ")[1]
    #record['casenumber'] = title[0].text.split(" Case No.")[1]
    print record
    #NEED TO ADD:
    #SAVING ON SCRAPERWIKI
    #SCRAPING PDF LINK ON THIS: http://www.italaw.com/cases/39
    #SCRAPING DOCS AT END OF THIS LINKED URL: http://www.italaw.com/cases/documents/1767
    

def scrape_table(root):
    links = root.cssselect("div.link-wrapper a")
    for link in links:
        print link.text_content()
        linkurl = link.attrib.get("href")
        print linkurl
        scrape_page('http://www.italaw.com'+linkurl)

def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)


#START HERE:
url = 'http://www.italaw.com/cases-by-respondent?field_case_respondent_tid=All'
scrape_and_look_for_next_link(url)
