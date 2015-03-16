#!/usr/bin/env python

import scraperwiki
import requests
import lxml.html

#all the URLs end in a number, so we just loop through those...
for i in range(350,401):
    #...and add to the end of the URL - using (str) to make it a string
    url = 'http://www.chequecentre.co.uk/stores/'+str(i)
    print 'Scraping:', url
    #scrape page into 'html'
    html = requests.get(url)
    #convert to lxml.html object
    root = lxml.html.fromstring(html.content)
    #We need to grab what's in <section class="main"><div>
    address = root.cssselect('section.main div')
    #There are actually two divs and we need the second - this just shows both in case we hit a problem
    for blah in address:
        print 'blah', blah.text_content()
    #print the second [1] div text content
    print 'address.text', address[1].text_content()
    #store that in 'fulladdress'
    fulladdress = address[1].text_content()
    #split it on the comma, this makes a list. Store the first item in that list - i.e. the bit before the first comma
    city = address[1].text_content().split(',')[0]
    #Store the last first item in that list - i.e. the bit after the last comma
    postcodefull = address[1].text_content().split(',')[-1]
    #Split the last bit on a space, and grab the second [1] item (after the first space)
    postcode1 = address[1].text_content().split(',')[-1].split(' ')[1]
    #Split the last bit on a space, and grab the third [2] item (after the first space)
    postcode2 = address[1].text_content().split(',')[-1].split(' ')[2]
    #Just in case there's anything else missed by the bit before and after the first comma, we grab that
    anythingelse = address[1].text_content().split(',')[1]
    #create an empty dict
    record = {}
    #store all the variables above in it
    record['url'] = url
    record['fulladdress'] = fulladdress
    record['city'] = city
    record['postcodefull'] = postcodefull
    record['postcode1'] = postcode1
    record['postcode2'] = postcode2
    record['anythingelse'] = anythingelse
    print 'record:', record
    #save it with url as the unique key
    scraperwiki.sql.save(['url'],record)

#we don't need to save it - we could append it to a list and just loop through that, adding to URL and grabbing latlong from postcodes api