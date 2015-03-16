#!/usr/bin/env python

import scraperwiki
import requests
import parslepy
import mechanize

#NEED TO GRAB NEXT PAGE - JAVASCRIPT
#ALSO RSS FEED SEEMS QUITE GOOD

#rules for finding the job data - used later
rules = {
    "job_links(div.leftcolumn)":[
        {
        "job_id":"div a",
        "job_title": "div#jobid",
        "job_link": "div a @href",
        "location": "div#location",
        "pay": "div#salary",
        "dates":"div#dates"
        }
    ]
}

#set our starting URL
url = "http://www.w4mpjobs.org/SearchJobs.aspx?search=unpaid"
html = requests.get(url)
#grab the rules created earlier and put into 'parselet'
parselet = parslepy.Parselet(rules)
#parse the text from our scraped page, using those rules, and put into 'jobs'
jobs = parselet.parse_fromstring(html.content)
#loop through the results
for job in jobs.get("job_links"):
    print job
    #assign various sub-rule results into fields in our dataset
    job["employer"] = job["job_title"].split(", for ")[1]
    job["job_title"] = job["job_title"].split(", for ")[0]
    splitdates = job["dates"].split(", closes on ")
    job["datefrom"] = splitdates[0].replace("Posted on ","")
    job["dateto"] = splitdates[1]
    job["pay"] = job["pay"].replace("Salary: ","")
    job["location"] = job["location"].replace("Location: ","")
    print job
    scraperwiki.sql.save(unique_keys=['job_link'], data=job)

#scrape these: 
'''Graduate Talent Pool
Internwise
Guardian Jobs
Enternships
Fashion Jobs
TotalJobs 
Gumtree
Inspiring Interns
Indeed
Dezeen'''
