#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
import scraperwiki
import json

#Twitter API credentials - these need adding
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""


def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	#Better to be api = tweepy.API(auth, parser=JSONParser())
	#See http://stackoverflow.com/questions/14856526/parsing-twitter-json-object-in-python
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	print "oldest: ", oldest
	print "alltweets[0]: ", alltweets[0]
	#Converts first tweet to text
	#see http://stackoverflow.com/questions/27900451/convert-tweepy-status-object-into-json
	json_str = json.dumps(alltweets[0]._json)
	#CONVERT TO LOOP TO DO SAME TO ALL TWEETS
	record = {}
	print "len(alltweets)", len(alltweets)
	for tweet in alltweets:
	    print "type(tweet)", type(tweet)
	    json_str = json.dumps(tweet._json)
	    print "type(tweet) 2", type(json_str)
	    print "json_str:", json_str
	    #Split tweet on commas to create an array
	    tweetarray = json_str.split(', "')
	    #tweetid2 = json_str.split('/status/')[1].split('/')[0]
	    tweetid = json_str.split('"id": ')[1].split(',')[0]
	    tweettxt = json_str.split('"text": ')[1].split(', "is_quote_status"')[0]
	    tweetdate = json_str.split('"created_at": "')[2].split('", "')[0]
	    name = json_str.split('"name": "')[1].split('", "')[0]
	    screenname = json_str.split('"screen_name": "')[1].split('", "')[0]
	    tweeturl = "https://twitter.com/"+screenname+"/status/"+tweetid
	    record['tweetid'] = tweetid
	    record['tweettxt'] = tweettxt
	    record['tweetdate'] = tweetdate
	    record['name'] = name
	    record['screenname'] = screenname#
	    record['tweeturl'] = tweeturl
	    print "record: ", record
	    scraperwiki.sql.save(['tweetid'], record)
    #keep grabbing tweets until there are no tweets left to grab

	while len(new_tweets) > 0:
		print "getting tweets before %s" % (oldest)
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweetss
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print "...%s tweets downloaded so far" % (len(alltweets))
		#transform the tweepy tweets into a 2D array that will populate the csv	
		#outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
		#need to convert to a dict before saving - could do it in the loop above rather than at end
		for tweet in alltweets:
		    print "type(tweet)", type(tweet)
		    json_str = json.dumps(tweet._json)
		    print "type(tweet) 2", type(json_str)
		    print "json_str:", json_str
		    tweetarray = json_str.split(', "')
		    tweetid = json_str.split('"id": ')[1].split(',')[0]
		    tweettxt = json_str.split('"text": ')[1].split(', "is_quote_status"')[0]
		    tweetdate = json_str.split('"created_at": "')[2].split('", "')[0]
		    name = json_str.split('"name": "')[1].split('", "')[0]
		    screenname = json_str.split('"screen_name": "')[1].split('", "')[0]
		    tweeturl = "https://twitter.com/"+screenname+"/status/"+tweetid
		    record['tweetid'] = tweetid
		    record['tweettxt'] = tweettxt
		    record['tweetdate'] = tweetdate
		    record['name'] = name
		    record['screenname'] = screenname#
		    record['tweeturl'] = tweeturl
		    print "record: ", record
		    scraperwiki.sql.save(['tweetid'], record)

#Add names as strings to this list
accountslist = [] 
for account in accountslist:
    if __name__ == '__main__':
    	#pass in the username of the account you want to download
    	get_all_tweets(account)

