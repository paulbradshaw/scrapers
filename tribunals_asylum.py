#!/usr/bin/env python

#Let's list the steps we need our scraper to go through:
# We need to cycle through a list of URLs like this: https://tribunalsdecisions.service.gov.uk/utiac?&page=1
# And on each page, grab the link to the decision page
# Then from each decision page we need to grab a series of pieces of info

import scraperwiki
import requests
import lxml.html
import urllib2
import urllib3.contrib.pyopenssl

import pdfminer 
#from pdfminer.pdfparser import PDFParser
#import xml.etree.ElementTree as ET


# We will need somewhere to store what we scrape
# So we create an empty dict variable called 'record', which we'll add to later


'''
def grabpdf(url):
    pdfdata = urllib2.urlopen(url).read()
    print "The pdf file has %d bytes" % len(pdfdata)
    xmldata = scraperwiki.pdftoxml(pdfdata)
    print "After converting to xml it has %d bytes" % len(xmldata)
    print "The first 2000 characters are: ", xmldata[:2000]
    #ValueError: Unicode strings with encoding declaration are not supported. Please use bytes input or XML fragments without declaration.
    #Found solution here: https://stackoverflow.com/questions/3224268/python-unicode-encode-error
    root = lxml.etree.fromstring(xmldata.encode('ascii', 'ignore'))
    #Can also try this https://docs.python.org/2/library/xml.etree.elementtree.html#module-xml.etree.ElementTree
    #tree = ET.fromstring(xmldata.encode('ascii', 'ignore'))
    pages = list(root)
    print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]
    decisiontextpdf = ''
    for page in pages:
        # print the first hundred text elements from the first page
        for el in list(page)[:100]:
            if el.tag == "text":
                print el.attrib
                print gettext_with_bi_tags(el)
                decisiontextpdf = gettext_with_bi_tags(el)+''+gettext_with_bi_tags(el)
                

#Do we need this function?
def findtext(root):
    # this line uses xpath to find <text tags
    lines = root.findall('.//text')
    print lines
    textlines = []
    for line in lines:
        print 'xpath version ', line.text
        if line:
            print 'NONE!'
        else: #This line needs to grab the text - may need function below
            textlines.append(line.text)
    newtextlines = " /n".join(textlines)
    print len(textlines)


#Create a function which drills down to bold and italic tags and grabs text
def gettext_with_bi_tags(el):
    res = []
    if el.text:
        res.append(el.text)
    for lel in el:
        res.append("<%s>" % lel.tag)
        res.append(gettext_with_bi_tags(lel))
        res.append("</%s>" % lel.tag)
        if el.tail:
            res.append(el.tail)
    return "".join(res)

url = "http://moj-tribunals-documents-prod.s3.amazonaws.com/decision/pdf_file/49656/00336_ukut_iac_2016_fj_pakistan.pdf"
grabpdf(url)
'''

record = {}

# Here we define a function to scrape the decision page
def grabdecisionpage(url):
    dicttoreturn = {}
    html = requests.get(url, verify=False)
    root = lxml.html.fromstring(html.content)
    # How do we select a property attribute? Google it! http://www.w3schools.com/cssref/css_selectors.asp
    keywords = root.cssselect('li span[property="keywords"]')[0].text
    print 'keywords ', keywords
    dicttoreturn['keywords'] = keywords
    #PDF versions of the decision are within a class="pdf-file"
    pdflink = root.cssselect('a.pdf-file')[0].attrib['href']
    print 'pdflink ', pdflink
    dicttoreturn['pdflink'] = pdflink
    #Word versions of the decision are within a class="doc-file"
    doclink = root.cssselect('a.doc-file')[0].attrib['href']
    print 'doclink ', doclink
    dicttoreturn['doclink'] = doclink
    # This either grabs 'an HTML version is not available' or 'The decision'
    nohtml = root.cssselect('div div:nth-child(2) h2')[0].text
    print nohtml
    dicttoreturn['nohtml'] = nohtml
    #These need checking against the results page
    country = root.cssselect('li span')[15].text
    print 'country', country
    dicttoreturn['country'] = country
    judges = root.cssselect('li span')[17].text
    print 'judges', judges
    dicttoreturn['judges'] = judges
    dates = root.cssselect('time[property="datePublished"]')
    print 'dates ', len(dates)
    for date in dates:
        print date.text
        print date.attrib['timedate']
    #Need to add date attributes, as encoded as proper dates (and store as such)
    dicttoreturn['hearingdate'] = dates[0].text
    dicttoreturn['promulgation'] = dates[1].text
    dicttoreturn['publication'] = dates[2].text
    dicttoreturn['updated'] = dates[3].text 
    dicttoreturn['hearingdate1'] = dates[0].attrib['timedate']
    dicttoreturn['promulgation1'] = dates[1].attrib['timedate']
    dicttoreturn['publication1'] = dates[2].attrib['timedate']
    dicttoreturn['updated1'] = dates[3].attrib['timedate'] 
    # The whole decision is within div class="decision-inner" and separated by <br/> tags
    if len(root.cssselect('div.decision-inner'))>0:
        decisiontext = root.cssselect('div.decision-inner')[0].text_content()
        #Because they are self closing <br/> tags we can't grab the contents (they close before they begin)
        #So each line is concatenated without a space.
        #We can still solve this, though, using the .tail function which grabs what comes *after* the tag.
        #First grab all the br tags into a list
        print 'length of decisiontext: ', len(decisiontext)
        dicttoreturn['decisiontext'] = decisiontext
        brs = root.cssselect('div.decision-inner br')
        #Create an empty string variable to add our results to
        decisiontextclean = ''
        #Then loop through that list
        for br in brs:
            print br.tail
            #Some lines are empty, so we need an if test first before using them
            if br.tail!=None:
                    decisiontextclean = decisiontextclean + br.tail+' <br />'
    else:
        decisiontext = 'NO TEXT'
        decisiontextclean = ''
    #print 'decisiontext:', decisiontext
    print 'len of decisiontextclean: ', len(decisiontextclean)
    dicttoreturn['decisiontextclean'] = decisiontextclean
    #Because this function is going to be called, we can choose to either:
    #return values to whatever called it (and store them there)
    #or call in values when running the function (and store them here)
    return dicttoreturn
    
grabdecisionpage('https://tribunalsdecisions.service.gov.uk/utiac/2016-ukut-336')
# Set our base URL which we'll add a number to
baseurl = 'http://tribunalsdecisions.service.gov.uk/utiac?&page='
# Luckily our URL only changes by adding a different number, from 1 to 403
# We can generate a list of those numbers using the RANGE function in Python
# See http://pythoncentral.io/pythons-range-function-explained/
# This takes 2 main arguments: where you want the range to start, and where you want it to end. 
pagelist = range(1,404)
# We set the end as 404 because it will stop just before that, at 403
# You can test that by adding a line saying print pagelist[-1] which will print the last item in the list

# Now we loop through our list of numbers
for page in pagelist:
    # And for each number, we add it to the baseurl to create a full url we store in a variable called 'resultsurl'
    # Now that needs to be a string, so along the way we need to convert the page number to a string using str()
    resultsurl = baseurl+str(page)
    print 'scraping', resultsurl
    # Now to fetch the page from that URL, using the requests library's 'get' function:
    html = requests.get(resultsurl, verify=False)
    # without verify got this error: requests.exceptions.SSLError: [Errno bad handshake] [('SSL routines', 'SSL3_GET_SERVER_CERTIFICATE', 'certificate verify failed')]
    # Googled, found this: https://stackoverflow.com/questions/10667960/python-requests-throwing-up-sslerror
    #To store it in a way that can be queried using lxml.html we use the 'fromtstring' function
    root = lxml.html.fromstring(html.content)
    # Now we can use cssselect to select based on css selectors
    # This will only grab the reported results. For unreported you need td.unreported
    decurls = root.cssselect('td.reported a')
    #Because there's more than one match, the result is a list, which we need to loop through
    '''for decurl in decurls:
        # We want the href attribute rather than text, which we grab using .attrib
        print decurl.attrib['href']
        # And now we store it in our 'record' variable
        record['url'] = decurl.attrib['href']
        fullurl = 'https://tribunalsdecisions.service.gov.uk'+decurl.attrib['href']
        record['refno'] = decurl.text
        record['status'] = 'reported'
        print record
        returneddict = grabdecisionpage(fullurl)
        print 'returneddict ', returneddict
        record['keywords'] = returneddict['keywords']
        record['nohtml'] = returneddict['nohtml']
        record['decisiontextclean'] = returneddict['decisiontextclean']
        record['pdflink'] = returneddict['pdflink']
        record['doclink'] = returneddict['doclink']
        record['country'] = returneddict['country']
        record['judges'] = returneddict['judges']
        record['hearingdate'] = returneddict['hearingdate']
        record['promulgation'] = returneddict['promulgation'] 
        record['publication'] = returneddict['publication'] 
        record['updated'] = returneddict['updated']
        record['YMDhearingdate'] = returneddict['hearingdate1']
        record['YMDpromulgation'] = returneddict['promulgation1'] 
        record['YMDpublication'] = returneddict['publication1'] 
        record['YMDupdated'] = returneddict['updated1']
        
        record['Yhearingdate'] = returneddict['hearingdate1'].split('-')[0]
        record['Mhearingdate'] = returneddict['hearingdate1'].split('-')[1]
        record['Dhearingdate'] = returneddict['hearingdate1'].split('-')[2]
        if returneddict['pdflink'] == decurl.attrib['href']:
            print 'NO PDF!'
        else:
            print 'INSERT PDF SCRAPING FUNCTION HERE'
        # Then we save that record variable in the scraperwiki sql database
        # You have to specify a unique key. In this case each url is different so we can use that as a unique key
        scraperwiki.sql.save(['url'],record)'''
    unreportedurls = root.cssselect('td.unreported a')
    for decurl in unreportedurls:
        # We want the href attribute rather than text, which we grab using .attrib
        print decurl.attrib['href']
        # And now we store it in our 'record' variable
        record['url'] = decurl.attrib['href']
        fullurl = 'https://tribunalsdecisions.service.gov.uk'+decurl.attrib['href']
        record['fullurl'] = fullurl
        record['refno'] = decurl.text
        record['status'] = 'unreported'
        print record
        #This runs the grabdecisionpage function on the fullurl
        #We can choose to send it our data and save to scraperwiki within that function...
        #Or return data back from that function and save it here
        
        
        # Then we save that record variable in the scraperwiki sql database
        # You have to specify a unique key. In this case each url is different so we can use that as a unique key
        scraperwiki.sql.save(['url'],record)



