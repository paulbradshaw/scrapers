#!/usr/bin/env python

#start at http://www.remotecentral.com/cgi-bin/codes
#add all links to brands to a list - e.g. http://www.remotecentral.com/cgi-bin/codes/3m/
#then loop through each and add all links to models to list2 - e.g. http://www.remotecentral.com/cgi-bin/codes/3m/8650_lcd/
#then grab all codes and associate with codes (e.g. Up)
#and go to 'next' link to repeat
import scraperwiki
import requests
import lxml.html

baseurl = 'http://www.remotecentral.com'

#new function to scrape the actual hexcodes
def scrapecodes(url,codesdata):
    print url
    print "length of URL",len(url)
    urllength = len(url)
    fullurl = baseurl+url
    html = requests.get(fullurl)
    root = lxml.html.fromstring(html.content)
    rowlinks = root.cssselect('tr td a')
    #empty list for the page numbers
    rowlinkpages = []
    #LOOP THROUGH AND IDENTIFY THE ONES WITH /PAGE- IN
    for rowlink in rowlinks:
        if '/page-' in rowlink.attrib['href']:
            #add the page number to the page number list
#ONLY WORKS IF PAGES <10
            rowlinkpages.append(int(rowlink.attrib['href'][-2:-1]))
        else:
            #otherwise append 1 because an empty list will generate an error
            rowlinkpages.append(1)
    #Once all page numbers have been added to list, find out biggest (last page)
    lastpagenumber = max(rowlinkpages)
    print "Biggest number in rowlinkpages list", lastpagenumber
    #generate a range from 1 to that last page - because the range function doesn't include the last value, add 1 to it
    pagerange = range(1,lastpagenumber+1)
    print "pagerange",pagerange
    #for each number in that range
    for page in pagerange:
        #create a url with that number at the end - it needs to be converted to string to work as url
        #some urls already have /page-1 in them so need to test for those & adjust accordingly
        print "DOES THIS SAY PAGE?", url[-7:-3]
        print "fullurl",fullurl
        print "baseurl",baseurl
        print "url",url
        print "str(page)",str(page)
        if url[-7:-3] == 'page':
            parturl = baseurl+url[:-7]
            fullurl = parturl+'page-'+str(page)
            print "fullurl = baseurl+url[-7:-3]+'-'+str(page)"
        else:
            fullurl = baseurl+url+'page-'+str(page)
            print "fullurl = baseurl+url+'page-'+str(page)",fullurl
        print "fullurl2",fullurl
        html = requests.get(fullurl)
        root = lxml.html.fromstring(html.content)
        #grab all the links in tables
        rowlinks = root.cssselect('tr td a')
    #The next line grabs the number of models in this html:
    #This model contains a total of <span class="bluetext">15</span> IR codes.
    #That number could be used as the end of a range to loop through - but if it's >20 then rest on other pages
        coderange = root.cssselect('span.bluetext')[0].text
        #grab all tables
        tables = root.cssselect('table')
        #grab all <tr> rows within the 15th [14] table
        rows = tables[14].cssselect('tr')
        #loop through those rows
        for row in rows:
            #some rows are blank, or header, so test if 'Copy to Clipboard' appears first:
            if 'Copy to Clipboard' in row.text_content():
                #then put in 'codesrow'
                codesrow = row.text_content()
                print "model?", url.split('/')[4]
                hexcodes = codesrow.split('(Copy to Clipboard)')[1]
                command = codesrow.split('(Copy to Clipboard)')[0]
                codesdata['codesrow'] = codesrow
                codesdata['hexcodes'] = hexcodes
                codesdata['command'] = command
                codesdata['url'] = fullurl
                codesdata['id'] = url+command
                codesdata['coderange'] = coderange
                codesdata['model'] = url.split('/')[4]
                codesdata['brand'] = url.split('/')[3]
                print "---", codesdata
                scraperwiki.sqlite.save(['id'], codesdata, 'codesdata')


#NEED TO ADD LINES TO GRAB 'NEXT' PAGES TOO
#THEN? SPLIT HEXCODE BY SPACES TO CREATE LIST IF NEEDED?
#STORE RESULTS - IGNORE TEMPLATE CODE BELOW
    # unique_keys = [ 'id' ]
    # data = { 'id':12, 'name':'violet', 'age':7 }
    # scraperwiki.sql.save(unique_keys, data)'''

#New function to grab links to models
def scrapemodels(url):
    codesdata = {}
    #print url
    #print "length of URL",len(url)
    #find out length of (relative) 'url' because we need this to generate a range later
    urllength = len(url)
    #create a full (absolute) url
    fullurl = baseurl+url
    html = requests.get(fullurl)
    #convert to lxml object
    root = lxml.html.fromstring(html.content)
    #LOOP THROUGH AND IDENTIFY THE ONES WITH /PAGE- IN
    #grab all the links in tables
    rowlinks = root.cssselect('tr td a')
    rowlinkpages = []
    #LOOP THROUGH AND IDENTIFY THE ONES WITH /PAGE- IN
    for rowlink in rowlinks:
        if '/page-' in rowlink.attrib['href']:
            #add the page number to the page number list
#ONLY WORKS IF PAGES <10
            rowlinkpages.append(int(rowlink.attrib['href'][-2:-1]))
        else:
            #otherwise append 1 because an empty list will generate an error
            rowlinkpages.append(1)
    #Once all page numbers have been added to list, find out biggest (last page)
    lastpagenumber = max(rowlinkpages)
    print "Biggest number in rowlinkpages list", lastpagenumber
    #generate a range from 1 to that last page - because the range function doesn't include the last value, add 1 to it
    pagerange = range(1,lastpagenumber+1)
    print "pagerange",pagerange
    #for each number in that range
    for page in pagerange:
        #create a url with that number at the end - it needs to be converted to string to work as url
        print "DOES THIS SAY PAGE? (First function)", url[-7:-3]
        fullurl = baseurl+url+'page-'+str(page)
        print "fullurl1",fullurl
        html = requests.get(fullurl)
        root = lxml.html.fromstring(html.content)
        #grab all the links in tables
        rowlinks = root.cssselect('tr td a')
    #create empty list to store our links in
        modelurllist = []
        #grab anything within <tr><td><a - example code below:
        #<tr><td class="brandindexcol1" align="center"><table width="55%" border="0" cellspacing="0" cellpadding="0"><tr valign="top"><td style="padding: 2px 10px 2px 0px;" align="right"><img src="/arw-blue.gif" width="9" height="17"></td><td class="text" style="padding: 2px 0px 2px 0px;"><a href="/cgi-bin/codes/3m/8650_lcd/">8650 LCD</a></td></tr>
        links = root.cssselect('tr td a')
    #NEED TO ADD LINES TO GRAB 'NEXT' PAGES TOO
        #loop through all the results:
        for link in links:
            #grab the href=" attribute
            linkurl = link.attrib['href']
            #print linkurl[0:urllength]
            #if the initial number of characters corresponding to the length of the relative url...
            #...are the same as the relative url
            if linkurl[0:urllength] == url:
                #then add to our previously empty list
                modelurllist.append(linkurl)
        #print "modelurllist", modelurllist
        #once loop has finished, loop through resulting list
        for modelurl in modelurllist:
            #run 'scrapecodes' function on each
            scrapecodes(modelurl,codesdata)

#Code below compiles a list of URLs from one page - commented out as the list is copied below
'''html = requests.get("http://www.remotecentral.com/cgi-bin/codes")
#convert into lxml object
root = lxml.html.fromstring(html.content)
#links look like this:
#<a href="/cgi-bin/codes/abb/">ABB</a> <span class="greytext smalltextc"><b>(<span class="bluetext">3</span>)</b></span><br>
#grab all items within <td><a
links = root.cssselect('td a')
#create empty list to store them in
brandurllist = []
#loop through list of grabbed lxml objects
for link in links:
    #print link.attrib['href']
    #grab href= attribute and put in 'url'
    url = link.attrib['href']
    #print url[0:15]
    #check first 15 chars - we only want links in /codes directory
    if url[0:15] == '/cgi-bin/codes/':
        #add them to our empty list if they are:
        brandurllist.append(url)
print "brandurllist",brandurllist'''

#already scraped: '/cgi-bin/codes/3m/', '/cgi-bin/codes/abb/', '/cgi-bin/codes/acer/', '/cgi-bin/codes/ada/', '/cgi-bin/codes/adcom/', '/cgi-bin/codes/aethra/', '/cgi-bin/codes/aiwa/', '/cgi-bin/codes/akai/', '/cgi-bin/codes/alpine/', '/cgi-bin/codes/amc/', '/cgi-bin/codes/ampro/', '/cgi-bin/codes/anthem/', '/cgi-bin/codes/apex/', '/cgi-bin/codes/apti/', '/cgi-bin/codes/aragon/', '/cgi-bin/codes/ask/', '/cgi-bin/codes/atlantic_technology/', '/cgi-bin/codes/audio_design_associates/', '/cgi-bin/codes/audio_ease/', '/cgi-bin/codes/audio_international/', '/cgi-bin/codes/audio_request/', '/cgi-bin/codes/audioaccess/', '/cgi-bin/codes/audioease/', '/cgi-bin/codes/audiosource/', '/cgi-bin/codes/auton/', '/cgi-bin/codes/auto-vue/', '/cgi-bin/codes/b_&_k/', '/cgi-bin/codes/bang_&_olufsen/', '/cgi-bin/codes/barco/', '/cgi-bin/codes/biamp/', '/cgi-bin/codes/bmb/', '/cgi-bin/codes/bogen/', '/cgi-bin/codes/bose/', '/cgi-bin/codes/broksonic/', '/cgi-bin/codes/btx/', '/cgi-bin/codes/california_audio_labs/', '/cgi-bin/codes/canon/', '/cgi-bin/codes/carver/', '/cgi-bin/codes/channel_master/', '/cgi-bin/codes/chaparral/', '/cgi-bin/codes/chiro/', '/cgi-bin/codes/chisholm/', '/cgi-bin/codes/christie_digital_systems/', '/cgi-bin/codes/clarion/', '/cgi-bin/codes/classe/', '/cgi-bin/codes/counterpoint/', '/cgi-bin/codes/ctx/', '/cgi-bin/codes/ctx-optima/', '/cgi-bin/codes/daewoo/', '/cgi-bin/codes/dalite/', '/cgi-bin/codes/davis/', '/cgi-bin/codes/dbox/', '/cgi-bin/codes/denon/', '/cgi-bin/codes/digital_projection/', '/cgi-bin/codes/dish_network/', '/cgi-bin/codes/dmx/', '/cgi-bin/codes/draper/', '/cgi-bin/codes/dual_cassette/', '/cgi-bin/codes/dukane/', '/cgi-bin/codes/dwin/', '/cgi-bin/codes/echostar/', '/cgi-bin/codes/eike/', '/cgi-bin/codes/eiki/', '/cgi-bin/codes/elan/', '/cgi-bin/codes/electrohome/', '/cgi-bin/codes/electronics/', '/cgi-bin/codes/elero/', '/cgi-bin/codes/elmo/', '/cgi-bin/codes/epson/', '/cgi-bin/codes/escient/', '/cgi-bin/codes/everquest/', '/cgi-bin/codes/extron/', '/cgi-bin/codes/fanfare/', '/cgi-bin/codes/fanon/', '/cgi-bin/codes/farenheit/', '/cgi-bin/codes/faroudja/', '/cgi-bin/codes/fisher/', '/cgi-bin/codes/fosgate_audionics/', '/cgi-bin/codes/fostex/', '/cgi-bin/codes/fox/', '/cgi-bin/codes/fujitsu/', '/cgi-bin/codes/funai/', '/cgi-bin/codes/ge/', '/cgi-bin/codes/gc_electronics/', '/cgi-bin/codes/general_instruments/', '/cgi-bin/codes/getner/', '/cgi-bin/codes/globecast/', '/cgi-bin/codes/go_video/', '/cgi-bin/codes/grand_channel/', '/cgi-bin/codes/grand_tech/', '/cgi-bin/codes/grundig/', '/cgi-bin/codes/harmon_kardon/', '/cgi-bin/codes/hitachi/', '/cgi-bin/codes/houston_tracking_systems/', '/cgi-bin/codes/hughes/', '/cgi-bin/codes/hunter_douglas/', '/cgi-bin/codes/imerge/', '/cgi-bin/codes/infocus/', '/cgi-bin/codes/integra/', '/cgi-bin/codes/i-point/', '/cgi-bin/codes/jaton/', '/cgi-bin/codes/jbl/', '/cgi-bin/codes/jerrold/', 
brandurllist = ['/cgi-bin/codes/jvc/', '/cgi-bin/codes/kds/', '/cgi-bin/codes/kenavision/', '/cgi-bin/codes/kenwood/', '/cgi-bin/codes/kinergetics_research/', '/cgi-bin/codes/kloss/', '/cgi-bin/codes/mtx/', '/cgi-bin/codes/kodak/', '/cgi-bin/codes/krell/', '/cgi-bin/codes/kustom/', '/cgi-bin/codes/lexicon/', '/cgi-bin/codes/linn/', '/cgi-bin/codes/litetouch/', '/cgi-bin/codes/loewe/', '/cgi-bin/codes/lutron/', '/cgi-bin/codes/luxman/', '/cgi-bin/codes/magnavox/', '/cgi-bin/codes/makita_electric_works/', '/cgi-bin/codes/marantz/', '/cgi-bin/codes/mark_levinson/', '/cgi-bin/codes/matrix_systems/', '/cgi-bin/codes/mcintosh/', '/cgi-bin/codes/mediland/', '/cgi-bin/codes/megapower/', '/cgi-bin/codes/meridian/', '/cgi-bin/codes/microsoft/', '/cgi-bin/codes/mindpath/', '/cgi-bin/codes/mitsubishi/', '/cgi-bin/codes/monivision/', '/cgi-bin/codes/monovision/', '/cgi-bin/codes/motorola/', '/cgi-bin/codes/multi_video_labs/', '/cgi-bin/codes/nad/', '/cgi-bin/codes/nakamichi/', '/cgi-bin/codes/nec/', '/cgi-bin/codes/netware/', '/cgi-bin/codes/nikko/', '/cgi-bin/codes/niles/', '/cgi-bin/codes/novaplex/', '/cgi-bin/codes/nsm/', '/cgi-bin/codes/nuview/', '/cgi-bin/codes/nview/', '/cgi-bin/codes/oak/', '/cgi-bin/codes/on_command/', '/cgi-bin/codes/ong_corporation/', '/cgi-bin/codes/onkyo/', '/cgi-bin/codes/pace/', '/cgi-bin/codes/pace_sky_manual/', '/cgi-bin/codes/panasat/', '/cgi-bin/codes/panasonic/', '/cgi-bin/codes/parasound/', '/cgi-bin/codes/philips/', '/cgi-bin/codes/piano_disc/', '/cgi-bin/codes/picturetel/', '/cgi-bin/codes/pinnacle/', '/cgi-bin/codes/pioneer/', '/cgi-bin/codes/plus/', '/cgi-bin/codes/poloroid/', '/cgi-bin/codes/polycom/', '/cgi-bin/codes/primare/', '/cgi-bin/codes/primestar/', '/cgi-bin/codes/princeton/', '/cgi-bin/codes/pro_presenter/', '/cgi-bin/codes/proceed/', '/cgi-bin/codes/projectavision/', '/cgi-bin/codes/proscan/', '/cgi-bin/codes/proton/', '/cgi-bin/codes/proxima/', '/cgi-bin/codes/qrs/', '/cgi-bin/codes/quasar/', '/cgi-bin/codes/rca/', '/cgi-bin/codes/replay_tv/', '/cgi-bin/codes/request_multimedia/', '/cgi-bin/codes/revox/', '/cgi-bin/codes/rft/', '/cgi-bin/codes/rock-ola/', '/cgi-bin/codes/rotel/', '/cgi-bin/codes/runco/', '/cgi-bin/codes/russound/', '/cgi-bin/codes/samsung/', '/cgi-bin/codes/sanyo/', '/cgi-bin/codes/scientific_atlanta/', '/cgi-bin/codes/sears/', '/cgi-bin/codes/seleco/', '/cgi-bin/codes/sharp/', '/cgi-bin/codes/sherwood/', '/cgi-bin/codes/silent_gliss/', '/cgi-bin/codes/sima/', '/cgi-bin/codes/sky/', '/cgi-bin/codes/somfy/', '/cgi-bin/codes/sony/', '/cgi-bin/codes/sonic_blue/', '/cgi-bin/codes/southerland/', '/cgi-bin/codes/sunfire/', '/cgi-bin/codes/sunteca/', '/cgi-bin/codes/tagmclaren/', '/cgi-bin/codes/tandberg/', '/cgi-bin/codes/tascam/', '/cgi-bin/codes/teac/', '/cgi-bin/codes/technics/', '/cgi-bin/codes/telex/', '/cgi-bin/codes/theta_casablanca/', '/cgi-bin/codes/theta_digital/', '/cgi-bin/codes/toshiba/', '/cgi-bin/codes/totevision/', '/cgi-bin/codes/travelors/', '/cgi-bin/codes/turtle_beach/', '/cgi-bin/codes/uniden/', '/cgi-bin/codes/us_electronics/', '/cgi-bin/codes/vantage/', '/cgi-bin/codes/vaux/', '/cgi-bin/codes/velodyne/', '/cgi-bin/codes/videolabs/', '/cgi-bin/codes/vidikron/', '/cgi-bin/codes/viewsonic/', '/cgi-bin/codes/viewtech/', '/cgi-bin/codes/vu-tec/', '/cgi-bin/codes/wireless_mouse_inc/', '/cgi-bin/codes/wisetech/', '/cgi-bin/codes/wolf/', '/cgi-bin/codes/x-10/', '/cgi-bin/codes/xantech/', '/cgi-bin/codes/yamaha/', '/cgi-bin/codes/zenith/']
for brandpage in brandurllist:
    scrapemodels(brandpage)

