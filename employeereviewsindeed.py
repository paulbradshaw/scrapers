#!/usr/bin/env python

import scraperwiki
import requests
import urllib2
import lxml.html
import json

baseurl = "https://www.indeed.co.uk"
#This URL is the search result...
starturl = "https://www.indeed.co.uk/charity-jobs"
#But when you move to page 2 it changes, so we need to use this instead to paginate
starturl = "https://www.indeed.co.uk/jobs?q=charity&start="

#create an empty record (this will be filled when the function runs above)
record = {}
#create an empty list to store URLs (see below - we use the datastore instead)
urllist = []

def scraperesultspage(resultsurl, urllist):
    print "SCRAPING", resultsurl
    html = scraperwiki.scrape(resultsurl)
    #convert it to an lxml object
    root = lxml.html.fromstring(html)
    print root
    #grab span tags with class attribute as specified
    companies = root.cssselect('span[class="company"] a')
    for company in companies:
        companyname = company.text_content()
        print companyname
        companyurl = company.attrib.get('href')
        print companyurl
        #this next line can be uncommented to scrape each company page...
        #scrapecompanypage(companyurl)
        #...However, because they appear more than once it's more efficient to store URLs first and get rid of duplicates
        #record['companyurl'] = companyurl
        #record['companyname'] = companyname
        #save to the datastore
        #scraperwiki.sqlite.save(['companyurl'], record, table_name='charities')
        #Another approach is to store items in a list which we can later convert to unique values only
        urllist.append(companyurl)
        print len(urllist)

def scrapecompanypage(companyurl):
    #The reviews view looks like this: https://www.indeed.co.uk/cmp/Together/reviews
    reviewsurl = baseurl+companyurl+"/reviews"
    print "SCRAPING", reviewsurl
    html = scraperwiki.scrape(reviewsurl)
    #convert it to an lxml object
    root = lxml.html.fromstring(html)
    print root
    #grab div tags with class attribute as specified - this will always be a list although there should only be 1
    companynames = root.cssselect('div.cmp-company-name')
    #Grab the first (and only) item from that list, and the text content of that tag, store in a variable
    companyname = companynames[0].text_content()
    #grab span tags with class attribute as specified
    reviews = root.cssselect('ul li.cmp-menu--reviews a div')
    reviewnum = reviews[0].text_content()
    print "reviews", reviewnum
    #print type(reviewnum)
    ratings = root.cssselect('span.cmp-average-rating')
    rating = float(ratings[0].text_content())
    print "rating", rating
    #print type(rating)
    #print type(reviewsurl)
    #There are 5 categories, but they all use the same tags
    categoryratings = root.cssselect('span.cmp-ReviewCategories-rating')
    categorynames = root.cssselect('span.cmp-ReviewCategories-name')
    #print 'How many?', len(categoryratings)
    #We use the headings to create field names and allocate the corresponding values to them
    #So the first field is given the first value and so on
    #This saves us having to write 5 different lines for each position, and also ensures values tally up with labels
    for i in range(0,len(categoryratings)):
        record[categorynames[i].text_content()] = categoryratings[i].text_content()
    #Same thing again for the counts of each rating
    ratingvalues = root.cssselect('span.cmp-ReviewHistogram-rating')
    ratingcounts = root.cssselect('span.cmp-ReviewHistogram-number')
    for i in range(0,len(ratingvalues)):
        record[ratingvalues[i].text_content()] = ratingcounts[i].text_content()
    #store the results in the 'record' dictionary variable
    record['reviewsurl'] = reviewsurl
    record['companyname'] = companyname
    record['reviews'] = reviewnum
    record['rating'] = rating
    #save to the datastore
    scraperwiki.sqlite.save(['reviewsurl'], record, table_name='reviews')

#We can then query the datastore for all URLs in the results, to use in another scrape
scrapedurljson = "https://premium.scraperwiki.com/x0hdcrq/mw20fbg1d0nharn/sql/?q=select%20companyurl%0Afrom%20charities"
#Fetch that URL using the urllib2 library
response = urllib2.urlopen(scrapedurljson)
#Read the JSON into a list variable using the json library
uniqueurls = json.loads(response.read())
print 'There are ', len(uniqueurls), ' URLs in our uniqueurls list'
#This is actually a list of dictionaries - 
print 'They look like this: ', uniqueurls[2]
#To drill into it you need to use an index for the item in the list and then the key for the value in the dictionary
print 'The URL looks like this: ', uniqueurls[2]['companyurl']
#So to loop through those we need to create a range of indexes from 0 to the number of the length of the list
for i in range(0,len(uniqueurls)):
    scrapecompanypage(uniqueurls[i]['companyurl'])
