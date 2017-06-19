#!/usr/bin/env python

import scraperwiki
import requests
import lxml.html

baseurl = 'http://musicbrainz.org/search?type=artist&method=indexed&query='
artists = ['T-rex','David Bowie','peter gabriel','tim blake','New Order','hawkwind','jackson browne','van morrison','ub40','curtis mayfield','the smiths','weather report','black uhuru','echo and the bunnymen','the boomtown rats','joe cocker','The Cure','level 42','psychedelic furs','the communards','elvis costello','suzanne vega','sinead o connor','happy mondays','youssou n dour','carter usm','shakespear s sister','lenny kravitz','christy moore','the black crowes','the levellers','Oasis','Pulp','The Prodigy','Radiohead','Ash','Primal Scream','Blur ','REM','Manic Street Preachers','Skunk Anansie','Chemical Brothers','Travis','Coldplay','Stereophonics','Rod Stewart','Moby','Paul McCartney ','Muse','The White Stripes','Basement Jaxx','Arctic Monkeys','The Killers','The Who ','Kings of Leon','Jaz-Z','The Verve','Neil Young','Bruce Springsteen','Gorillaz','Stevie Wonder','U2','Beyonce','The Rolling Stones','Mumford & Sons','Arcade Fire','Metallica ','Kasabian','Florence and the Machine','Kanye West','Adele','Foo Fighters','The Charlatans','Paul Weller','Bryan Adams','Faithless','Snow Patrol','Kaiser Chiefs','The Sex Pistols','The Police','The Strokes','Tom Petty and the Heartbreakers','Pearl Jam','The Stone Roses','Bon Jovi','Boy George','Calvin Harriss','Red Hot Chili Peppers','Billy Idol','Fleetwood Mac','Queen with Adam Lambert','David Guetta','Run DMC','Antony and the Johnsons','Mogwai','Damien Rice','The Good, The Bad and The Queen','Franz Ferdinand','Sigur Ros','Interpol','Pet Shop Boys','Grace Jones','Nick Cave and the Bad Seeds','Belle and Sebastian','Vampire Weekend','The National','Paolo Nutini','Suede','Bon Iver','Elbow','Bloc Party','Kraftwerk','Foals','Lily Allen','Damon Albarn','The Black Keys','alt-J','Portishead','Noel Gallagher s High Flying Birds','The Maccabees','The 1975','Mumford and Sons','Fleet Foxes','Jimmy Page and Robert Plant','Beastie Boys','Garbage','Charlatans','Eminem','Linkin Park','Green Day ','The Darkness','Pixies','Iron Maiden','Razorlight','The Smashing Pumpkins','Rage Against the Machine','Guns n Roses','Blink 182','My Chemical Romance','Biffy Clyro','Queens of the Stone Age','The Libertines','kim wilde','gloria gaynor','tony hadley','the human league','holly johnson','OMD','kool and  the gang','big country','the B-52s','the pointer sisters','billy ocean','daryl hall and john oates','thompson twins','andy bell','adam ant','midge ure','soul 2 soul','m people','Blur','Green Day','The Who','rihanna','Calvin Harris','avicii','richard ashcroft','texas','scissor sisters','morrissey','justin timberlake','justin bieber','pink','jay-z','keane','james blunt','david gray','massive attack','depeche mode','daft punk','counting crows','fatboy slim','lcd soundsystem','the black eyed peas','drake','deadmau5','bruno mars','rudimental','nicki minaj','kygo','chase & status','chance the rapper','the weeknd','skepta','mylo','norman jay','groove armada','jamiroquai','sly and the family stone','the flaming lips','manu chao','duran duran','dizzee rascal','roxy music','the wombats','snoop dogg','friendly fires','hot chip','azealia banks','plan b','goldfrapp','M.I.A','Nas','major lazer','frank ocean','the subways','funeral for a friend','the zutons','the pigeon detectives','super furry animals','cypress hill','the streets','newton faulkner','seasick steve','leftfield','klaxons','bombay bicycle club','ed sheeran','ben howard','the vaccines','bastille','james bay','two door cinema club','will young','jools holland','robert plant','blondie','crowded house','paul simon','sugababes','scouting for girls','status quo','the faces','james morrison','bellowhead','katzenjammer','squeeze','simple minds','the gypsy kings','roger hodgson','the jacques','king b','jamie cullum','seal','bryan ferry','the pretenders','audioslave','Metallica','feeder','system of a down','black sabbath','tool','Lostprophets','The Offspring','KISS','Slipknot','Faith no More','Def Leppard','AC/DC','Aerosmith','rammstein','Avenged sevenfold','josh ritter','badly drawn boy','lambchop','ryan adams','yo la tengo','conor oberst','mercury rev','calexico','steve earle','explosions in the sky','wilco','modest mouse','beirut','joanna newsom','grizzly bear','beach house','grandaddy','david byrne & st vincent','st vincent','wild beasts','tame impala','the war on drugs','sufjan stevens','bat for lashes','animal collective','father john misty','lucinda williams','mac Demarco']

def grabpic(url):
    html = requests.get(url, verify = False) # verify = False cause there is a security error https
    print html
#transform the html into lxml
    root = lxml.html.fromstring(html.content) #we need to add the word content
    # start using css selectors
    imgs = root.cssselect('img')
    print 'found', len(imgs), 'images'
    for img in imgs:
        print img.attrib['src']
        #fullurl = 'http://musicbrainz.org/'+firsturl.attrib['href']
    if len(root.cssselect('div.picture img')) != 0:
        img = root.cssselect('div.picture img')[0].attrib['src']
    else:
        img = 'NO IMAGE FOUND'
    print 'last image: ', img
    if img[:4] != "http":
        img = "http:"+img
    return img

def grabids(url):
    html = requests.get(url, verify = False) # verify = False cause there is a security error https
    print html
#transform the html into lxml
    root = lxml.html.fromstring(html.content) #we need to add the word content
    # start using css selectors
    lis = root.cssselect('li a')
    print len(lis)
    spotify = 'No link found'
    wikipedia = 'No link found'
    for li in lis:
        #print li.attrib['href']
        if li.attrib['href'][:24] == "http://open.spotify.com/":
            print 'SPOTIFY'
            spotify = li.attrib['href']
        if li.attrib['href'][:18] == "//en.wikipedia.org":
            print 'WIKIPEDIA'
            wikipedia = li.attrib['href']
    idlist = []
    idlist.append(spotify)
    idlist.append(wikipedia)
    return idlist

def grabwiki(url):
    print 'running grabwiki function...'
    html = requests.get(url, verify = False) # verify = False cause there is a security error https
    print html
    root = lxml.html.fromstring(html.content) #we need to add the word content
    # start using css selectors
    tds = root.cssselect('td a.image img')
    print len(tds)
    for td in tds:
        print td.attrib['src']
    return 'http:'+tds[0].attrib['src']

record = {}
for artist in artists[49:]:
    print 'looking for ', artist
    artisturl = baseurl+artist
    html = requests.get(artisturl, verify = False) # verify = False cause there is a security error https
    print html
#transform the html into lxml
    root = lxml.html.fromstring(html.content) 
    # start using css selectors
    firsturl = root.cssselect('td a')[0]
    print firsturl.attrib['href']
    fullurl = 'http://musicbrainz.org'+firsturl.attrib['href']
    wikiurl = grabids(fullurl)[1]
    record['artist'] = artist
    record['searchurl'] = artisturl
    record['musicbrainzurl'] = fullurl
    record['pic'] = grabpic(fullurl)
    record['spotify'] = grabids(fullurl)[0]
    record['wikipedia'] = wikiurl
    #record['wikipic'] = grabwiki('http:'+wikiurl)
    print record
    scraperwiki.sql.save(['musicbrainzurl'], record)


