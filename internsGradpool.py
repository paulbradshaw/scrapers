#!/usr/bin/env python

import scraperwiki
import requests
import mechanize

#Use mechanize to grab each page of results - or just last 50 from:
#https://graduatetalentpoolsearch.direct.gov.uk/casa/servlet/casa.jobseeker.JSVacServlet?mode=search
#Then job has static URL with id like 
#?mode=showVac&CASA_object_id=PVSUB-HIL4576-VACY-02092013-1891971

#FIRST DRAFT SCRAPER
url = 'https://graduatetalentpoolsearch.direct.gov.uk/casa/servlet/casa.jobseeker.JSVacServlet?mode=search'
html = requests.get('https://graduatetalentpoolsearch.direct.gov.uk/casa/servlet/casa.jobseeker.JSVacServlet?mode=showVac&CASA_object_id=PVSUB-HIL4576-VACY-02092013-1891971&search_level=&vacancy_class=W&ticket=EDA8CA8D-9309-4CE7-ACED-1EB49B2FDA01&from=21&total=328&curr_pos=21&last_pos=200&sortby=P&noofjobs=200')
print html.content
br = mechanize.Browser()
br.addheaders = [('user-agent', '   Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.3) Gecko/20100423 Ubuntu/10.04 (lucid) Firefox/3.6.3')]
#ignore the robots.txt, which prevents the scraper working - see http://stackoverflow.com/questions/2846105/screen-scraping-getting-around-http-error-403-request-disallowed-by-robots-tx
br.set_handle_robots(False)
response = br.open(url)
br.select_form(name='form1')
br['params'] = ['&search_level=&vacancy_class=&ticket=B361B433-E9E3-4CE4-A35F-9C0B1084A25A&from=1&total=0']
print br.form
response = br.submit()
print "RESPONSE", response.read()

#SECOND DRAFT SCRAPER
url = 'http://www.enternships.com/internships'
br = mechanize.Browser()
br.addheaders = [('user-agent', '   Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.3) Gecko/20100423 Ubuntu/10.04 (lucid) Firefox/3.6.3')]
br.set_handle_robots(False)
response = br.open(url)
print response.read()
html = requests.get(url)
print html.content
root = lxml.html.fromstring(html.content)
job_titles = root.cssselect('h2')
for title in job_titles:
    print "TITLE", title.text

# scraperwiki.sql.save(unique_keys, data)
