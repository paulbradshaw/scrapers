#!/usr/bin/env python

import scraperwiki
import requests
import mechanize
import lxml.html

#NEED TO GRAB NEXT PAGE - JAVASCRIPT

#set our starting URL
url = "http://www.w4mpjobs.org/SearchJobs.aspx?search=unpaid"
#create a fake browser with mechanize, called 'br'
br = mechanize.Browser()
response = br.open(url)
#select the form
br.select_form(name='aspnetForm')
#print the fields
print br.form
#in the field with the name in first square brackets, select the value in the second brackets
br['ctl00$MainContent$RadioButtonList2'] = ['9999']
br['ctl00$MainContent$rblSalary'] = ['unpaid']
#submit the form
response = br.submit()
#put the results of using .read on 'response' into 'html'
html = response.read()
#convert into lxml object
root = lxml.html.fromstring(html)
#grab all <div class='leftcolumn ...>, and put into 'jobs'
jobs = root.cssselect('div.leftcolumn')
#create an empty record to save into
record = {}
#loop through each job and split out details to save
for job in jobs:
    #assign various sub-rule results into fields in our dataset
    record["employer"] = job.cssselect('div#jobid')[0].text_content().split(", for ")[1]
    record["job_title"] = job.cssselect('div#jobid')[0].text_content().split(", for ")[0]
    splitdates = job.cssselect('div#dates')[0].text_content().split(", closes on ")
    record["datefrom"] = splitdates[0].replace("Posted on ","")
    record["dateto"] = splitdates[1]
    print record
    record["pay"] = job.cssselect('div#salary')[0].text_content().replace("Salary: ","")
    record["location"] = job.cssselect('div#location')[0].text_content().replace("Location: ","")
    record["job_id"] = job.cssselect('div a')[0].text_content()
    record["job_link"] = job.cssselect('div a')[0].attrib.get('href')
    scraperwiki.sql.save(unique_keys=['job_id'], data=record)

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
