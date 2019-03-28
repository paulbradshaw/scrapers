#import the libraries we'll need
import re
import scraperwiki
import urllib2
import lxml.etree
import lxml.html

#search URL is e.g. https://www.google.co.uk/search?q=site%3Abirminghammail.co.uk+%22Hannah+Sophia%22
baseurl = "https://www.google.co.uk/search?q="
siteoperator = "site%3A"
siteurl = "birminghammail.co.uk"
quotationmark = "%22"
paging = "&start="
#scrape_and_look_for_next_link(starting_url)

def scraperesultspage(url):
  record = {}
  headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
  timeout=0.25
  req = urllib2.Request(url, None, headers)
  #adapting some of the code from https://stackoverflow.com/questions/3569152/parsing-html-with-lxml
  doc = lxml.html.parse(urllib2.urlopen(req))
  links = doc.xpath('//h3/a')
  results = doc.xpath('//div[@id="resultStats"]') #//*[@id="resultStats"]
  print results[0].text_content()
  #print 'there are ', len(links), 'links'
  for link in links:
      linkhref = link.attrib['href']
      #print linkhref[:7]
      if linkhref[:7] != "/search":
          #print 'NOT SEARCH URL'
          #/search?q=site:
          record['url'] = linkhref
          scraperwiki.sqlite.save(['url'], record, table_name="candidatesearch")
  #This gives a number of results, e.g. 22000
  resultnum = int(results[0].text_content().split(' ')[1].replace(',',''))
  #pagenum = (resultnum/10)+1
  #print pagenum
  #print resultnum
  #pagination adds &start=10, 20 etc. so we need to generate a list of those numbers
  pagelist = range(0,resultnum,10)
  for pagenum in pagelist[1:]:
      print 'scraping results starting at,', pagenum
      scrapefurtherpage(pagenum, url)

def scrapefurtherpage(pagenum, url):
  fullpageurl = url+paging+str(pagenum)
  print 'pageurl?', fullpageurl
  #this duplicates code from earlier
  record = {}
  headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
  timeout=0.25
  req = urllib2.Request(fullpageurl, None, headers)
  #adapting some of the code from https://stackoverflow.com/questions/3569152/parsing-html-with-lxml
  doc = lxml.html.parse(urllib2.urlopen(req))
  links = doc.xpath('//h3/a')
  #results = doc.xpath('//div[@id="resultStats"]') #//*[@id="resultStats"]
  #print results[0].text_content()
  #print 'there are ', len(links), 'links'
  for link in links:
      linkhref = link.attrib['href']
      #print linkhref[:7]
      if linkhref[:7] != "/search":
          record['url'] = linkhref
          scraperwiki.sqlite.save(['url'], record, table_name="candidatesearch")

#url = "https://www.google.co.uk/search?q=site%3Abirminghammail.co.uk+%22david+ratcliff%22"
#url = "https://www.google.co.uk/search?q=site%3Abirminghammail.co.uk+%22david+ratcliff%22&start=90"
candidates = ['Andrew Mitchell','Rob Pocock','Hannah Sophia','Jennifer Wilkinson','david ratcliff']
for candidate in candidates[1:]:
searchurl = baseurl+siteoperator+siteurl+"+"+quotationmark+candidate.replace(' ','+')+quotationmark
print 'scraping', searchurl
scraperesultspage(searchurl)
