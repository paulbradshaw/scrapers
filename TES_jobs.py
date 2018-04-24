#!/usr/bin/env python

import scraperwiki
import requests
import urllib2
import lxml.html



#For testing - empty search
fullurl = "http://www.tes.com/jobs/search?area=jobs&sort=&keywords="
#This needs a number adding to the end
pageurl = "https://www.tes.com/jobs/search?area=jobs&sort=&keywords=&currentpage="

#Create a function to scrape a search results page
def scrape_listings(url):
    #Turn the page into an lxml object to scrape
    html = requests.get(url, verify=False)
    root = lxml.html.fromstring(html.content)
    #create empty dict to store data
    record = {}
    #jbos are contained within a link with <a class="t-job-link container-link__link">
    joblinks = root.cssselect("a.t-job-link.container-link__link")
    for job in joblinks:
        print job.attrib['href']
        joburl = job.attrib['href']
        headings = job.cssselect("h3")
        title = headings[0].text_content()
        employers = job.cssselect("div span span")
        school = employers[0].text_content()
        if len(employers)>0:
            try:
                location = employers[1].text_content()
            except:
                location = "No location given"
        salaries = job.cssselect("span.t-job-salary")
        print title, school, location
        if len(salaries)>0:
            salary = salaries[0].text_content()
        else:
            salary = "No salary shown"
        print salary
        record['title'] = title
        record['school'] = school
        record['location'] = location
        record['salary'] = salary
        record['joburl'] = joburl
        print record
        scraperwiki.sqlite.save(['joburl'], record)

#The count of jobs is within <span class="text--sm no-margin t-page-heading">
#Or there's a link to the last page of results in <a class="tes-btn tes-btn--secondary "
html = requests.get("https://www.tes.com/jobs/search?area=jobs&sort=&keywords=", verify=False)
root = lxml.html.fromstring(html.content)
#Find the links to the next pages
pageslinks = root.cssselect("a.tes-btn.tes-btn--secondary")
#The last page link will have the number of that page
lastpage = int(pageslinks[-1].text_content())

#Currently there are 2664 jobs, which means 134 pages (20 per page)
#But now we use the variable of the last page to grab that
for i in range(1,lastpage):
    print 'there are ', lastpage, ' pages of results'
    print 'scraping page ', i
    scrape_listings(pageurl+str(i))


