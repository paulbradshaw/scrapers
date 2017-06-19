#!/usr/bin/env python

import scraperwiki
import requests
import lxml.html

#example URL: http://www.nhs.uk/Services/hospitals/Services/Service/DefaultView.aspx?id=288035
baseurl = "http://www.nhs.uk/Services/hospitals/Services/Service/DefaultView.aspx?id="
ids = []
for idno in range(288035,289035):
    ids.append(str(id))
idno = 288035
html = requests.get(baseurl+str(idno)).content
#print html.content
root = lxml.html.fromstring(html)
openingtimes = root.cssselect('#ctl00_ctl00_ctl00_PlaceHolderMain_contentColumn1 > div.panel.panel-nonedit.module.general-info > div > div > div table')
print openingtimes[0].text_content()
timecells = openingtimes[0].cssselect('td meta')
print 'there are ', len(timecells), 'times listed'
#timecells = openingtimes[0].cssselect('th')
#print 'there are ', len(timecells), 'days listed'

record = {}
for cell in timecells:
    print cell.text_content()
    print cell.attrib['content']
    day = cell.attrib['content'][0:2]
    opentime = cell.attrib['content'][3:8]
    closetime = cell.attrib['content'][9:14]
    print opentime
    print closetime
    record['opentime'] = opentime
    record['closetime'] = closetime
    record['day'] = day
    record['id'] = idno
    record['idday'] = str(idno)+day
    print record
    scraperwiki.sql.save(['idday'], record)
