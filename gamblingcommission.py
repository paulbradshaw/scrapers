#!/usr/bin/env python

#This cycles through press releases looking for those related to enforcement
#tasks
#1. fetch links from news page
#2. grab details from link page
#3. find next page and repeat

#Create a variable to store the base url - we'll need this to add relative urls to
baseurl = "http://www.gamblingcommission.gov.uk"
#The News page allows you to select categories. This URL limits results to those involving enforcement action
propurl = "http://www.gamblingcommission.gov.uk/news-action-and-statistics/news/news.aspx?searchKeywords=&categories=0/1/24/41&page="

#import the libraries we'll need
import scraperwiki
import urllib2
import lxml.etree
import lxml.html
import requests

# these settings are for when request is used below
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
timeout=0.25

#create an empty record to store data
record = {}
#This function scrapes a results page - and then runs another function in the middle
def grablinks(url):
    print 'RUNNING GRABLINKS ON ', url
    html = requests.get(url, verify=False, timeout=timeout, headers=headers) #verify False to avoid the SSL error for security reasons
    #turn url into lxml object
    root = lxml.html.fromstring(html.content)
    #find link
    newslinks = root.cssselect('a.post.post--alt') 
    #cssselect always creates a list, so we need to loop through it
    for link in newslinks:
        #show the href= attribute
        linkhref = link.attrib['href']
        print linkhref
        #run the scrapepage function (defined below) on this url
        scrapepage(linkhref)

#This function scrapes an individual room page
def scrapepage(url):
    print 'RUNNING SCRAPEPAGE'
    #this line is for when we loop through errorsnodups which are already fully formed URLs like https://www.spareroom.co.uk/flatshare/london/stratford/7233100
    #url = url.split('https://www.spareroom.co.uk')[1]
    fullurl = baseurl+url
    print 'DIRTY URL? ', fullurl
    print 'SCRAPING ', fullurl
    #turn to lxml object
    # I think they're blocking repeated attempts to access, so...
    html = requests.get(fullurl, verify=False, timeout=timeout, headers=headers) #verify False to avoid the SSL error for security reasons
    #turn url into lxml object
    root = lxml.html.fromstring(html.content)
    #find the 5th table class='featurestable' and all the row cells in that
    ps = root.cssselect('p')
    h1s = root.cssselect('h1')
    headline = h1s[0].text
    print 'firstpar ', ps[0].text
    print 'pars ', len(ps)
    #cssselect always creates a list, so we need to loop through it
    fulltext = ""
    for i in range(0,len(ps)):
        fulltext = fulltext+ps[i].text_content()+" \n"
        record['statementurl'] = "NO STATEMENT LINK"
        plinks = ps[i].cssselect('a')
        #grab all links and test if they contain a statement link
        for plink in plinks:
            #For some reason this url throws a KeyError here: http://www.gamblingcommission.gov.uk/news-action-and-statistics/news/2014/Weaknesses-persist-in-underage-gambling-controls.aspx
            #So we add a try command to deal with that
            try:
                if "public-statements" in plink.attrib['href']:
                    print "GOTCHA"
                    #Overwrite the variable with an actual statement link
                    record['statementurl'] = baseurl+plink.attrib['href']
            except KeyError:
                print "KeyError"
        record['url'] = baseurl+url
        record['intro'] = ps[0].text_content()
        record['lastpar'] = ps[i-1].text_content()
        record['fulltext'] = fulltext
        record['headline'] = headline
        lis = root.cssselect('ol li')
        scraperwiki.sqlite.save(['url'],record)


#There are 198 news items, and 10 per page. So there are 20 pages of news items if you want to grab them all.
#In this category there are 55 items, so 6 pages
#The pages all end in page=1, page=2 etc. So we need to generate those numbers
for p in range(1,7):
    print 'scraping: ', propurl+str(p)
    #p is a number so we need to convert it to a string before adding to the URL
    #That URL is then used for the 'grablinks' function defined above
    grablinks(propurl+str(p))
