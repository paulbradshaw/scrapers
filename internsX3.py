#!/usr/bin/env python

import scraperwiki
import requests
import lxml.html

#first 2 functions work on one site, second 2 on another, and so on

#this function grabs links from fashionjobs site, then runs a second function on them
def fashionjobs_links(url):
    html = requests.get(url)
    root = lxml.html.fromstring(html.content)
    #select contents of all <li><a ...> tags
    job_links = root.cssselect('li a')
    #loop through each, call it 'link'
    for link in job_links:
        #if the href attribute of link contains this url (the part of the site for jobs)
        if 'http://uk.fashionjobs.com/job/' in link.attrib.get('href'):
            print "SCRAPING", link.attrib.get('href')
            #run the scrape_fashionjob function defined below, and put 'returned' results into 'record'
            record = scrape_fashionjob(link.attrib.get('href'))
            #add an extra field to that 'record'
            record['job_link'] = link.attrib.get('href')
            print "---", record
            #save it
            scraperwiki.sql.save(['job_link'], record)

#new function to scrape job page
def scrape_fashionjob(url):
    html = requests.get(url)
    root = lxml.html.fromstring(html.content)
    #create an empty record
    record = {}
    #next 3 lines grab & store the contents of first <h1>, <h3> and <time> tags respectively
    record['job_title'] = root.cssselect('h1')[0].text_content()
    record['employer'] = root.cssselect('h3')[0].text_content()
    record['postdate'] = root.cssselect('time')[0].text_content()
    #the headings are in <dt> tags in <div class="inner"> - grab them all
    headingslxml = root.cssselect('div.inner dt')
    #create an empty list to store the text versions in
    headings = []
    #loop through the list of lxml objects, grab text contents and append to that new list
    for heading in headingslxml:
        headings.append(heading.text_content())
    #the details are in <dd> tags in <div class="inner"> - grab them all
    valueslxml = root.cssselect('div.inner dd')
    #as above, the next few lines convert that lxml list into a text list
    values = []
    for value in valueslxml:
        values.append(value.text_content())
    print headings
    #We need to compare our headings list to one of all known possible headings 
    possibleheadings = ['Country','Region','Town','Contract type','Availability','Salary','Years experience','Language','Starting date']
    #work out which headings are NOT on the page - we'll use this to check whether to store them later
    headingsmissing = list(set(possibleheadings)-set(headings))
    print "Headings missing:", headingsmissing
    #As the information appears in different orders, 
    #we use the index position of the heading to grab the respective values
    record['country'] = values[headings.index('Country')]
    record['region'] = values[headings.index('Region')]
    record['location'] = values[headings.index('Town')]
    record['type'] = values[headings.index('Contract type')]
    record['hours'] = values[headings.index('Availability')]
    #Some fields are not always there, so we check them against our list of missing headings
    if 'Salary' not in headingsmissing:
        record['remuneration'] = values[headings.index('Salary')]
    else:
        record['remuneration'] = "NO INFORMATION"
    record['experience'] = values[headings.index('Years experience')]
    if 'Starting date' not in headingsmissing:
        record['available'] = values[headings.index('Starting date')]
    else:
        record['available'] = "NO INFORMATION"
    if 'Language' not in headingsmissing:
        record['languages'] = values[headings.index('Language')]
    else:
        record['languages'] = "NO INFORMATION"
    print "SCRAPED", record
    #return the full record to the variable = in the line which called this function
    return record

#loop through the 3 URLs containing job ad links
for i in range(1,4):
    url = 'http://uk.fashionjobs.com/s/?page='+str(i)+'&metier=&auto=0&msId=&secteur[]=1&secteur[]=2&secteur[]=3&categorie=&region=&soc=&contrat[]=5&emploi[]=1&emploi[]=2'
    #run the function defined above on that URL
    fashionjobs_links(url)


def inspiring_interns(url):
    html = requests.get(url)
    root = lxml.html.fromstring(html.content)
    #<div class="span-11">
    jobs = root.cssselect('div.span-11 h2 a')
    for job in jobs:
        print job.attrib.get('href')
        job_link = 'http://www.inspiringinterns.com/'+job.attrib.get('href')
        record = scrape_inspiring_interns(job_link)
        record['job_link'] = job_link
        scraperwiki.sql.save(['job_link'], record)

def scrape_inspiring_interns(url):
    html = requests.get(url)
    root = lxml.html.fromstring(html.content)
    job_details = root.cssselect('div#brief_info_NOCSS')
    record = {}
    for detail in job_details:
        record['job_title'] = detail.cssselect('h3')[0].text_content()
        record['available'] = detail.cssselect('td')[1].text_content()
        record['sector'] = detail.cssselect('td')[3].text_content()
        record['languages'] = detail.cssselect('td')[5].text_content()
        record['period'] = detail.cssselect('td')[7].text_content()
        record['location'] = detail.cssselect('td')[9].text_content()
        record['type'] = detail.cssselect('td')[11].text_content()
        record['hours'] = detail.cssselect('td')[13].text_content()
        record['remuneration'] = detail.cssselect('td')[15].text_content()
        print "SCRAPED", record
        return record

for i in range(1,11):
    inspiring_interns('http://www.inspiringinterns.com/interns/internship-offers/?page='+str(i))

def scrape_job_page(url):
    html = requests.get(url)
    root = lxml.html.fromstring(html.content)
    #grab contents of <td class="data">
    info = root.cssselect('td.data')
    record = {}
    for dd in info:
        record['job_title'] = dd.cssselect('h2')[0].text_content()
        record['job_link'] = dd.cssselect('h2 a')[0].attrib.get('href')
        record['employer'] = dd.cssselect('dd')[0].text_content()
        record['employer_link'] = dd.cssselect('dd a')[0].attrib.get('href')
        record['region'] = dd.cssselect('dd')[1].text_content()
        record['location'] = dd.cssselect('dd')[2].text_content()
        record['sector'] = dd.cssselect('dd')[3].text_content()
        record['period'] = dd.cssselect('dd')[4].text_content()
        record['type'] = dd.cssselect('dd')[5].text_content()
        record['remuneration'] = dd.cssselect('dd')[6].text_content()
        record['postdate'] = dd.cssselect('dd')[7].text_content()
        return record

def grab_internwise_links(url):
    html = requests.get(url)
    root = lxml.html.fromstring(html.content)
    links = root.cssselect('td.data h2 a')
    for link in links:
        print link.attrib.get('href')
        if 'http://www.internwise.co.uk/events/details/' in link.attrib.get('href'):
            print "THIS IS ONE!"
            record = scrape_job_page(link.attrib.get('href'))
            print record
            scraperwiki.sql.save(['job_link'], record)

#grab_internwise_links('http://www.internwise.co.uk/')
for i in range(1,10):
    grab_internwise_links('http://www.internwise.co.uk/events/search/b67fmc622cxcrhtd5ajtx73pbhpc7p7c/'+str(i))

keywords = ['Work+experience', 'volunteer', 'voluntary', 'Voluntary+worker', 'unpaid', 'expenses']


