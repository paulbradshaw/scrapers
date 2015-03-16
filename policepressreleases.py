#!/usr/bin/env python

import scraperwiki
import requests
import parslepy

rules = {
    "headlines(div#Main_ctl00_news table tr)":[
        {
        "link": "a @href",
        "title": "a",
        "date":"em",
        }
    ]
}

rules2 = {
    "content(div#Main_mainblock table)":[
        {
        "headline":"table td",
        "date":"em",
        "fulltext":"tr[1] td[0]"
        }
    ]
}

def scraperelease(releaseurl):
    html = requests.get(releaseurl)
    parselet = parslepy.Parselet(rules2)
    content = parselet.parse_fromstring(html.content)
    print content
    for contents in content.get("content"):
        print contents

def scrapeurl(url):
    html = requests.get(url)
    #print html.content
    #Links contained within <div id="Main_ctl00_news"><table><tr><td><a    
    parselet = parslepy.Parselet(rules)
    headlines = parselet.parse_fromstring(html.content)
    print headlines
    for headline in headlines.get("headlines"):
        print headline
        if headline['link']:
            print "FULLURL", "www.northants.police.uk/"+headline['link']
            releaseurl = "http://www.northants.police.uk/"+headline['link']
            scraperelease(releaseurl)
        #scraperwiki.sql.save(unique_keys=['link'], data=headline)


#http://www.northants.police.uk/default.aspx?id=news&type=archiveprego&month=1&year=2009
for num in range(2009,2014):
    year = str(num)
    for num2 in range(1,13):
        month = str(num2)
        url = "http://www.northants.police.uk/default.aspx?id=news&type=archiveprego&month="+month+"&year="+year
        print url
        scrapeurl(url)


# Saving data:
# unique_keys = [ 'id' ]
# data = { 'id':12, 'name':'violet', 'age':7 }
# scraperwiki.sql.save(unique_keys, data)
