#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import scraperwiki
import json

#Twitter API credentials
consumer_key = "NEEDSTOBEFILLED"
consumer_secret = "NEEDSTOBEFILLED"
access_key = "NEEDSTOBEFILLED"
access_secret = "NEEDSTOBEFILLED"



auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)
#Better to be api = tweepy.API(auth, parser=JSONParser())
#See http://stackoverflow.com/questions/14856526/parsing-twitter-json-object-in-python

record ={}
#See https://stackoverflow.com/questions/25895321/how-to-extract-hashtags-from-tweepy-using-tweepy-cursor-and-api-search
# see http://docs.tweepy.org/en/latest/api.html#help-methods
def scrape_hashtags(hashtag):
    for tweet in tweepy.Cursor(api.search, q=hashtag, lang="en").items(1000):
        tweettxt = tweet.text.encode('utf-8')
        tweetname = tweet.author.name
        print "Name:", tweetname
        print "Tweet:", tweettxt
        hashtags = tweet.entities.get('hashtags')
        print hashtags
        timestamp = tweet.created_at
        print "datestamp:", timestamp
        timestamptime = timestamp.time()
        timestampdate = timestamp.date()
        print "datestamp:", timestamp
        record['name'] = tweetname
        record['tweetxt'] = tweettxt.decode('utf-8')
        record['tweetid'] = tweet.id
        record ['tweetdate'] = timestampdate
        record ['tweettime'] = str(timestamptime)
        record ['hashtag'] = hashtag
        #record ['tweettxt'] = tweet.text
        print record
        scraperwiki.sql.save(['tweetid'], record)

hashtagslist = ['#casino','#slots','#odds','#betinplay', '#poker', '#freebets']
for hashtag in hashtagslist:
    scrape_hashtags(hashtag)

