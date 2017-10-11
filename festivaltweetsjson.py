#!/usr/bin/env python

import json
import csv
import requests
import urllib
import scraperwiki

jsonurlgh = 'https://raw.githubusercontent.com/paulbradshaw/scraping-for-everyone/gh-pages/webpages/cheltenhamjazz-export.json'
jsonurl = 'https://paulbradshaw.github.io/scraping-for-everyone/webpages/cheltenhamjazz-export.json'
trumpjson = 'https://petition.parliament.uk/petitions/178844.json'

#fetch the json from the URL
response = urllib.urlopen(jsonurl)
#load it into variable called x
x = json.loads(response.read())
#let's see what we have
print x
print len(x)
#drill down a bit into the 'posts' branch which contains everything
print x['posts']
#store that in a new variable
posts = x['posts']
#how many items?
print len(x['posts'])
#this only grabs the ID number of each
#create an empty list to store the ID numbers, which we can then loop through to grab each tweet
postids = []
for post in posts:
    print post
    postids.append(post)
#create empty dict to store the data
record = {}
#loop through the codes
for code in postids:
    print x['posts'][code]
    #test that we can grab the text
    print x['posts'][code]['text']
    #start storing each field in the dict
    record['text'] = x['posts'][code]['text']
    record['authorid'] = x['posts'][code]['author']
    try:
        record['imageurl'] = x['posts'][code]['image']
    except KeyError:
        record['imageurl'] = 'NULL'
    record['lon'] = x['posts'][code]['lon']
    record['lat'] = x['posts'][code]['lat']
    record['timestamp'] = x['posts'][code]['timestamp']
    #this is the tweet code that we are using
    record['tweetid'] = code
    record['fulljson'] = str(x['posts'][code])
    scraperwiki.sql.save(['tweetid'], record)

