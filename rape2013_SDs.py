#!/usr/bin/env python

import scraperwiki
import requests
import urllib2
import lxml.etree

# this function has to work recursively because we might have "<b>Part1 <i>part 2</i></b>"
def gettext_with_bi_tags(el):
    res = [ ]
    if el.text:
        res.append(el.text)
    for lel in el:
        res.append("<%s>" % lel.tag)
        res.append(gettext_with_bi_tags(lel))
        res.append("</%s>" % lel.tag)
        if el.tail:
            res.append(el.tail)
    return "".join(res)

#Define a new function called 'scrapepdf' with one parameter: 'pdfurl'
def scrapepdf(pdfurl):
    #use the .urlopen function from urllib library (imported at the start of this scraper) to open 
    #and the .read method to read into new variable 'pdfdata'
    pdfdata = urllib2.urlopen(pdfurl).read()
    #convert to an XML object so we can scrape using lxml.etree
    xmldata = scraperwiki.pdftoxml(pdfdata)
    #grab the first 30 characters [:30]
    print "The first 30 characters are: ", xmldata[:30]
    #convert into an lxml object
    root = lxml.etree.fromstring(xmldata)
    #use the list function to get a list of pages
    pages = list(root)
    print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]
    page71 = pages[69]
    p71data = []
    for el in list(page71)[:100]:
        if el.tag == "text":
            print el.attrib, gettext_with_bi_tags(el)
            p71data.append(gettext_with_bi_tags(el))
    print 'p71data so far:', p71data
    return p71data

#This list was compiled using the Chrome Scraper addon, 
#then cleaned in Google Drive using =SUBSTITUTE to replace the common parts of the URL with ""
#and combined into a list using =JOIN("','",C2:C44)
#a quick test run shows the Metropolitan entry is wrong, so manually fixed

forcelist = ['avon-and-somerset','bedfordshire','cambridgeshire','cheshire','city-of-london','cleveland','cumbria','derbyshire','devon-and-cornwall','dorset','durham','dyfed-powys','essex','gloucestershire','greater-manchester','gwent','hampshire','hertfordshire','humberside','kent','lancashire','leicestershire','lincolnshire','merseyside','metropolitan','norfolk','north-wales','north-yorkshire','northamptonshire','northumbria','nottinghamshire','south-wales','south-yorkshire','staffordshire','suffolk','surrey','sussex','thames-valley','warwickshire','west-mercia','west-midlands','west-yorkshire','wiltshire']
#testlist - to be deleted later
#forcelist = ['metropolitan','norfolk']
record = {}
#loop through each force name
for force in forcelist:
    #insert it into the standard URL format for the PDFs
    pdfurl = "http://www.hmic.gov.uk/media/" + force + "-value-for-money-profile-2013.pdf"
    print pdfurl
    #Run the scrapepdf function (defined previously) on that URL
    p71data = scrapepdf(pdfurl)
    print "returned data", p71data
    record['source'] = pdfurl
    record['forceurl'] = force
    record['pagetitle'] = p71data[0]
    record['offence1'] = p71data[4]
    record['rapeOffences1213'] = p71data[5]
    record['rapeSDs1213'] = p71data[6]
    record['rapePerc'] = p71data[7]
    record['rapeMSG'] = p71data[8]
    record['rapeDiff'] = p71data[9]
    record['offence2'] = p71data[10]
    record['otherSexOff1213'] = p71data[11]
    record['otherSD'] = p71data[12]
    record['otherPerc'] = p71data[13]
    record['OtherMSG'] = p71data[14]
    record['otherDiff'] = p71data[15]
    record['offence3'] = p71data[16]
    record['SexOffencesTotal1213'] = p71data[17]
    record['SexOffencesSDs'] = p71data[18]
    record['SexOffencesPerc'] = p71data[19]
    record['SexOffencesMsg'] = p71data[20]
    record['SexOffencesExp'] = p71data[21]
    record['Police force'] = p71data[24]
    print record
    scraperwiki.sql.save(['forceurl'],record)
    

