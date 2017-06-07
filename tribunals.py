#!/usr/bin/env python
#!/usr/bin/env python

# loop through a list of URLs
# grab 10 links from each URL
# go to each link and grab info, including PDF/doc URL
# ? go to PDF URL and grab info
# ? go to doc URL and grab info

import scraperwiki
import requests
import lxml.html

baseurl = 'http://tribunalsdecisions.service.gov.uk/utiac?&page='
#create a list with range. Write the URL without the page number

#after the loops create a new variable to get the information
def grabdecisionspage (url):
    mylist = [] #create an empty list to store the elements
    firsturl = 'https://tribunalsdecisions.service.gov.uk' #url without the end of every court ruling
    decisionurl = firsturl+url # join the end and the url
    html = requests.get(decisionurl, verify=False) #verify False to avoid the SSL error for secutiry reasons
    root = lxml.html.fromstring(html.content)
    #repeat to get the rest of the info changing the css selector and instead of attrib['href'] write .text
    pdflinks = root.cssselect('a.pdf-file') #cssselect always creates a list 
    pdflink = pdflinks[0].attrib['href'] #specify the element in the list [0] the first one in that case. If there is no element, it would generate an error. Then we would need a if - len 
    doclinks = root.cssselect('a.doc-file')
    doclink = doclinks[0].attrib['href'] 
    caseinfo = root.cssselect('span[property="name"]')
    casedetail = caseinfo[0].text
    dates = root.cssselect('li:nth-child(5) > span:nth-child(2) > time')
    date = dates[0].text_content()
    print pdflink
    print doclink
    print casedetail
    print date
    mylist.append(pdflink)
    mylist.append(doclink)
    mylist.append(casedetail)
    mylist.append(date)
    
    thedecisions = root.cssselect('div.decision-inner')
    print thedecisions
    if thedecisions != []: #!= not equal
        thedecision = thedecisions[0].text_content()
        print thedecision
    else: #get nothing and go on
        thedecision = ''
    mylist.append(thedecision)
    
    countries = root.cssselect('li:nth-child(8) > span:nth-child(2)')
    if countries != []: #!= not equal
        country = countries[0].text_content()
        print country
    else: #get nothing and go on
        country = ''
    
    mylist.append(country)
    
    judges = root.cssselect('li:nth-child(9) > span:nth-child(2)')#content > div > div:nth-child(2) > header > ul > li:nth-child(9) > span:nth-child(2)
    if judges != []: #!= not equal
        judge = judges[0].text_content()
        print judge
    else: #get nothing and go on
        judge = ''
    mylist.append(judge)
    
    return mylist


pagelist = range (1,408) #PROBLEMS WITH THE RANGE!!!! create a list of numbers to complete the URl
record = {} #create a dictionary

# get the 405 URL page url + number 
for n in pagelist: #loop into the page list
    allurls = baseurl + str(n)
    print allurls
    html = requests.get(allurls, verify = False) # verify = False cause there is a security error https
    print html
#transform the html into lxml
    root = lxml.html.fromstring(html.content) #we need to add the word content
    # start using css selectors
    repandunrepurls = root.cssselect('td a') # the tag in the page is <td class="reported"> ... <a href We need the a to get all the content
    # Options: decurls = root.cssselect('tr a') because there is only one table
    print len(repandunrepurls) #it indicates in the code how long it's what we want to scrape
 
    
    for elements in repandunrepurls : #loop in the URL pages to get the elements inside
        print elements.attrib['href'] #get the links
        repandunrepurls = elements.attrib['href'] #put the links inside a variable
        #order of the columns 
        mylist = grabdecisionspage(repandunrepurls)
        record['pdf'] = mylist[0]
        record ['doc'] = mylist[1]
        record['case'] = mylist[2]
        record['date'] = mylist[3]
        record['decision'] = mylist[4]
        record['country'] = mylist[5]
        record['judge'] = mylist[6]
        #record ['pdfurl'] = pdfurl
        record['url'] = repandunrepurls
        #record['status'] = repandunrepurls.text #this is a string/text we will add as we know the tag reported is the same as the text
        record ['id'] = elements.text 
        scraperwiki.sql.save(['url'], record)
  
'''
    for unrepurl in unrepurls : # the same loop for the unreported
        print unrepurl.attrib['href']
        unreporturl = unrepurl.attrib['href']
        mylist = grabdecisionspage(unreporturl)
        record['pdf'] = mylist[0]
        record ['doc'] = mylist[1]
        record['case'] = mylist[2]
        record['date'] = mylist[3]
        record['decision'] = mylist[4]
        record['country'] = mylist[5]
        record['judge'] = mylist[6]
        record['url'] = unreporturl
        record['status'] = 'unreported'
        record ['id'] = unrepurl.text 
        scraperwiki.sql.save(['url'], record)
'''

# Saving data:
# unique_keys = [ 'id' ]
# data = { 'id':12, 'name':'violet', 'age':7 }
# scraperwiki.sql.save(unique_keys, data)
