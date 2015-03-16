#!/usr/bin/env python

import scraperwiki
html = scraperwiki.scrape('http://uk.soccerway.com/teams/netherlands/fortuna-sittard/1551/')
#print html

import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
tds = root.cssselect('table.table.squad.sortable tr td') # get all the cells in that table - each is a player
#print tds
indexno = 0
for td in tds: #loop through the players
    indexno = indexno+1
    fullentry = lxml.html.tostring(td)
    player = fullentry.split("</a>")[0]
    player = player.split(">")[-1]
    print "fullentry",fullentry
    agelist = fullentry.split("27px")
    applist = fullentry.split('title="Appearances"')
    goallist = fullentry.split('title="Goal"')
    #<span class="flag_16 right_16 netherlands_16_right">
    #nationality = fullentry.split("flag")
    spans = td.cssselect('div span')
    flag = ""
    for span in spans:
        print "SPAN", span.attrib['class']
        nationality = span.attrib['class'].replace("flag_16 right_16 ","").replace("_16_right","").replace("-"," ")
        print nationality
        flag = nationality
    if len(agelist) > 1:
        age = agelist[1].split("<")[0].replace(';">','')
        print "age", age
    else:
        age = ""
    if len(applist) > 1:
        apps = applist[1].split("<")[0].replace("> ","")
        print "apps", apps
    else:
        apps = ""
    if len(goallist) > 1:
        goals = goallist[1].split("<")[0].replace("> ","")
        print "goals", goals
    else:
        goals = ""
    record = {"td":fullentry,"name":player,"age":age,"apps":apps,"goals":goals,"flag":flag,"index":indexno}
    print "---", record
    scraperwiki.sql.save(["index"],record)
