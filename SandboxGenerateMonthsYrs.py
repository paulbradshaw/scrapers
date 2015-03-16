#!/usr/bin/env python

import scraperwiki
import requests
import parslepy
import urllib
import urlparse

#this sets the rules for content we want on the first page (list of headlines)
rules = {
    "headlines(div#Main_ctl00_news table tr)":[
        {
        "link": "a @href",
        "title": "a",
        "date":"em",
        }
    ]
}

#this sets the rules for what we want on the actual press release page
rules2 = {
    # there is an embedded <table> in the first row,
    # so the ">" CSS operator is used to match only the immediate child
    # see http://www.w3.org/TR/css3-selectors/#child-combinators
    "content(div#Main_mainblock > table)":[
        {
        "headline":"table td",
        # using parslepy's XPath extension parsley:strnl() -- note prefix "parsley", not "parslepy"
        # (newer version handle parsley and parslepy prefixes as aliases to one another)
        # it will convert <br> and other black HTML elements to a "\n" newline character
        # it makes the output more readable
        # NOTE: this works ony for XPath expressions (for now)
        "date":"parsley:strnl(.//em)",
        #"fulltext":"tr[1] td[0]" would be natural,
        # but doesnt work unfortunately as CSS selector
        # it's safer to use XPath, and first position is position 1
        "fulltext":"parsley:strnl(./tr[2]/td[1])"
        }
    ]
}

# as the rules do not change
# it's more efficient to create the Parselets once
url_parselet = parslepy.Parselet(rules)
release_parselet = parslepy.Parselet(rules2)

#define a function to scrape the press release page
def scraperelease(releaseurl):
    html = requests.get(releaseurl)
    #use the rules above to grab content
    content = release_parselet.parse_fromstring(html.content)
    print content
    #grab the 'content' part of rules2 above (a list), and loop through
    for contents in content.get("content"):
        print contents
        scraperwiki.sql.save(unique_keys=['link'], data=contents)


#define a function to scrape the pages linking to press releases
def scrapeurl(url):
    html = requests.get(url)
    #print html.content
    #Links contained within <div id="Main_ctl00_news"><table><tr><td><a    
    #use rules from rules = ... above
    headlines = url_parselet.parse_fromstring(html.content)
    print headlines
    #loop through the 'headlines' part of 'rules' (a list)
    for headline in headlines.get("headlines"):
        print headline
        if headline['link']:
            # urlparse.urljoin() makes it more readable
            # and handles more cases ("../../link", "/link", "./link" etc.)
            releaseurl = urlparse.urljoin(url, headline['link'])
            print "FULLURL", releaseurl
            scraperelease(releaseurl)
        #uncomment this if you only want to save the headlines, dates, links
        #scraperwiki.sql.save(unique_keys=['link'], data=headline)
 
 
#http://www.northants.police.uk/default.aspx?id=news&type=archiveprego&month=1&year=2009
# when using more than 1 or 2 query parameters
# [Paul Tremberth] finds it easier to use urllib's urlencode() method
query_parameters = {
    "id": "news",
    "type": "archiveprego",
    "month": "",
    "year": "",
}
for num in range(2009,2014):
    query_parameters["year"] = str(num)
    for num2 in range(1,13):
        query_parameters["month"] = str(num2)
        query_string = urllib.urlencode(query_parameters)
        url = "http://www.northants.police.uk/default.aspx?%s" % query_string
        print url
        scrapeurl(url)
 
 
