#!/usr/bin/env python

import scraperwiki
import requests
import urllib2
import lxml.etree

#URL lists and base URL at the bottom of scraper

checklist = ['http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/blackpool.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/cornwall.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/ealing.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/hackney.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/islington.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/leicestershire.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/northamptonshire.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/north-lincolnshire.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/north-east-lincolnshire.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/north-tyneside.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/shropshire.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/suffolk.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/warrington.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/west-sussex.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/wirral.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/worcestershire.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/halton.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/kingston-upon-hull.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/oldham.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/sandwell.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/stoke-on-trent.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/walsall.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/bexley.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/bath-and-north-east-somerset.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/barking-and-dagenham.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/barnet.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/bedford.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/barnsley.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/bournemouth.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/brent.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/blackburn-with-darwen.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/brighton-and-hove.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/bolton.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/bristol.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/bromley.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/bury.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/buckinghamshire.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/cheshire-east.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/cambridgeshire.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/calderdale.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/central-bedfordshire.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/cheshire-west-and-chester.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/camden.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/coventry.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/croydon.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/darlington.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/cumbria.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/derby.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/devon.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/derbyshire.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/doncaster.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/durham.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/dudley.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/east-sussex.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/dorset.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/essex.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/gateshead.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/enfield.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/gloucestershire.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/greenwich.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/hammersmith-and-fulham.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/hampshire.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/harrow.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/herefordshire.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/hillingdon.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/havering.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/hertfordshire.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/isle-of-wight.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/hounslow.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/kent.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/kensington-and-chelsea.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/lambeth.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/lancashire.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/kingston-upon-thames.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/lewisham.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/leicester.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/lincolnshire.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/leeds.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/luton.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/medway.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/merton.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/newham.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/north-somerset.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/northumberland.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/manchester.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/nottingham.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/north-yorkshire.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/nottinghamshire.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/oxfordshire.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/portsmouth.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/redbridge.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/peterborough.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/plymouth.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/reading.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/richmond-upon-thames.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/redcar-and-cleveland.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/rochdale.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/salford.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/sefton.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/sheffield.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/somerset.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/slough.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/solihull.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/southampton.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/south-tyneside.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/southend-on-sea.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/south-gloucestershire.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/southwark.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/staffordshire.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/st-helens.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/stockton-on-tees.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/stockport.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/sutton.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/surrey.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/swindon.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/torbay.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/tameside.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/tower-hamlets.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/telford-and-wrekin.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/thurrock.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/wandsworth.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/wakefield.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/waltham-forest.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/trafford.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/westminster.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/warwickshire.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/wolverhampton.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/wiltshire.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/york.pdf','http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/newcastle-upon-tyne.pdf']

def grabtext(line):
    if '<i>' in line:
        linetext = line.split('i>')[1].split('<')[0]
    else:
        linetext = line.split('>')[1].split('<')[0]
    return linetext

#Define a new function called 'scrapepdf' with 1 parameters: 'pdfurl' 
def scrapepdf(pdfurl, year):
    #use the .urlopen function from urllib library (imported at the start of this scraper) to open 
    #and the .read method to read into new variable 'pdfdata'
    #try:
    pdfdata = urllib2.urlopen(pdfurl).read()
    #convert to an XML object so we can scrape using lxml.etree
    xmldata = scraperwiki.pdftoxml(pdfdata)
    #these lines throw up an error:
    #ValueError: Unicode strings with encoding declaration are not supported. Please use bytes input or XML fragments without declaration.
    #root = lxml.etree.fromstring(xmldata)
    #Split to grab the pages with volunteer data. This needs to be put in separate function
    volunteerspage = xmldata.split('A5: Electronic Workstations')[1]
    pagelines = volunteerspage.split('<text')
    #Because around a third of results don't get captured in that block, the next line just does the same for the whole doc
    doclines = xmldata.split('<text')
    indexline = -1
    perthou = 'CHECK THIS'
    aveperthou = 'CHECK THIS'
    issuesnum = 'CHECK THIS'
    #wifipoints = 'NOT GRABBED'
    hrsperthou = 'NOT GRABBED'
    hrsrecorded = 'NOT GRABBED'
    terminals = 'NOT GRABBED'
    hrsper100thou = 'NOT GRABBED'
    termper100thou = 'NOT GRABBED'
    hrsavilable = 'NOT GRABBED'
    wifipoints = 'NOT GRABBED'
    #this is a counter which goes up for each match it finds (later in the if loop)
    #we hope this ends up 1 in the final spreadsheet to indicate only one thing at that position in the whole doc
    perthouNODUP = 0
    aveperthouNODUP = 0
    hrsavailNODUP = 0
    terminalsNODUP = 0
    hrsrecordedNODUP = 0
    hrsperthouNODUP = 0
    wifipointsNODUP = 0
    #termper100thou = 0
    numberpos = 0
    hrsrecordedYpos = 0
    for line in doclines:
        indexline = indexline+1
        if 'Service Points with Wi-Fi Access' in line:
            print 'WHAT IS THE TOP POS?', line
            print 'WHAT IS THE LINE BEFORE?', doclines[indexline-1]
            print 'WHAT IS THE LINE AFTER?', doclines[indexline+1]
            print "NUMBER OF LINES", len(pagelines)
        #in 2014 reports terminal hours figures are at top=420 or 419
        if 'top="420"' in line or 'top="419"' in line and year==2014:
            print "FOUND", line
            if 'left="184"' in line:
                hrsrecorded = grabtext(line)
                hrsrecordedNODUP = hrsrecordedNODUP+1
                hrsrecordedYpos = 184
            elif 'left="189"' in line:
                hrsrecorded = grabtext(line)
                hrsrecordedNODUP = hrsrecordedNODUP+1
                hrsrecordedYpos = 189
            if 'left="318"' in line:
                hrsperthou = grabtext(line)
                hrsperthouNODUP = hrsperthouNODUP+1
                hrsperthouYpos = 318
            elif 'left="306"' in line:
                hrsperthou = grabtext(line)
                hrsperthouNODUP = hrsperthouNODUP+1
                hrsperthouYpos = 306
            if 'left="701"' in line and '%' in line:
                wifipoints = grabtext(line)
                wifipointsNODUP = wifipointsNODUP+1
                wifipointsYpos = 701
            elif 'left="694"' in line and '%' in line:
                wifipoints = grabtext(line)
                wifipointsNODUP = wifipointsNODUP+1
                wifipointsYpos = 694
            elif 'left="686"' in line and '%' in line:
                wifipoints = grabtext(line)
                wifipointsNODUP = wifipointsNODUP+1
                wifipointsYpos = 686
        if 'top="430"' in line or 'top="433"' in line and year==2012:
            print "FOUND", line
            if 'left="176"' in line:
                hrsrecorded = grabtext(line)
                hrsrecordedNODUP = hrsrecordedNODUP+1
                hrsrecordedYpos = 176
            elif 'left="184"' in line:
                hrsrecorded = grabtext(line)
                hrsrecordedNODUP = hrsrecordedNODUP+1
                hrsrecordedYpos = 184
            if 'left="301"' in line:
                hrsperthou = grabtext(line)
                hrsperthouNODUP = hrsperthouNODUP+1
                hrsperthouYpos = 301
            elif 'left="289"' in line:
                hrsperthou = grabtext(line)
                hrsperthouNODUP = hrsperthouNODUP+1
                hrsperthouYpos = 289
            if 'left="731"' in line and '%' in line:
                wifipoints = grabtext(line)
                wifipointsNODUP = wifipointsNODUP+1
                wifipointsYpos = 731
            elif 'left="739"' in line and '%' in line:
                wifipoints = grabtext(line)
                wifipointsNODUP = wifipointsNODUP+1
                wifipointsYpos = 739
            elif 'left="724"' in line and '%' in line:
                wifipoints = grabtext(line)
                wifipointsNODUP = wifipointsNODUP+1
                wifipointsYpos = 724
        #The terminals figures are top=107
        if 'top="107"' in line or 'top="110"' in line and year==2012:
            print "FOUND", line
            if 'left="328"' in line and year==2014:
                termper100thou = line.split('>')[1].split('<')[0]
                perthouNODUP = perthouNODUP+1
            elif 'left="320"' in line:
                termper100thou = line.split('>')[1].split('<')[0]
                perthouNODUP = perthouNODUP+1
            elif 'left="325"' in line and year==2012:
                termper100thou = line.split('>')[1].split('<')[0]
                perthouNODUP = perthouNODUP+1
            elif 'left="318"' in line and year==2012:
                termper100thou = line.split('>')[1].split('<')[0]
                perthouNODUP = perthouNODUP+1
            if 'left="703"' in line:
                hrsper100thou = line.split('>')[1].split('<')[0]
                aveperthouNODUP = aveperthouNODUP+1
            elif 'left="715"' in line:
                hrsper100thou = line.split('>')[1].split('<')[0]
                aveperthouNODUP = aveperthouNODUP+1
            elif 'left="711"' in line and year==2012:
                hrsper100thou = line.split('>')[1].split('<')[0]
                aveperthouNODUP = aveperthouNODUP+1
            elif 'left="723"' in line and year==2012:
                hrsper100thou = line.split('>')[1].split('<')[0]
                aveperthouNODUP = aveperthouNODUP+1
            if 'left="579"' in line:
                hrsavilable = line.split('>')[1].split('<')[0]
                hrsavailNODUP = hrsavailNODUP+1
            elif 'left="582"' in line and year==2012:
                hrsavilable = line.split('>')[1].split('<')[0]
                hrsavailNODUP = hrsavailNODUP+1
            if 'left="203"' in line and year==2012:
                terminals = line.split('>')[1].split('<')[0]
                terminalsNODUP = terminalsNODUP+1
            elif 'left="209"' in line and year==2014:
                terminals = line.split('>')[1].split('<')[0]
                terminalsNODUP = terminalsNODUP+1
            elif 'left="216"' in line:
                terminals = line.split('>')[1].split('<')[0]
                terminalsNODUP = terminalsNODUP+1
            elif 'left="211"' in line:
                terminals = line.split('>')[1].split('<')[0]
                terminalsNODUP = terminalsNODUP+1
    record['yr'] = year
    record['Terminals'] = terminals
    record['Terminals per 100,000'] = termper100thou
    record['Hours available per 1,000'] = hrsper100thou
    record['Hours available'] = hrsavilable
    record['pdfurl'] = pdfurl
    authority = 'TESTING'
    if year==2012:
        authority = pdfurl.replace(for2012,'').replace('.pdf','').replace('-', ' ').replace('%20', ' ')
    elif year==2014:
        authority = pdfurl.replace('http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/','').replace('.pdf','').replace('-', ' ').replace('%20', ' ')
    record['authority'] = authority.title()
    record['Terminals per 100k'] = perthouNODUP
    record['terminals CHECK'] = terminalsNODUP
    record['Hrs recorded per K CHECK'] = hrsperthouNODUP
    record['Hrs avail per K CHECK'] = aveperthouNODUP
    record['wifipoints CHECK'] = wifipointsNODUP
    record['hrs recorded CHECK'] = hrsrecordedNODUP
    record['hr available CHECK'] = hrsavailNODUP
    record['hrsrecorded'] = hrsrecorded
    record['hours per thousand pop'] = hrsperthou
    record['% service points with wifi'] = wifipoints
    record['wifi Y pos'] = wifipointsYpos
    if terminalsNODUP > 0 or hrsperthouNODUP > 0 or wifipointsNODUP > 0 or hrsrecordedNODUP > 0 or hrsavailNODUP > 0 or hrsperthouNODUP > 0:
        errorlist.append(pdfurl)
    print record
    scraperwiki.sql.save(['pdfurl'],record)
    print 'errorlist', errorlist


record = {}
pdfurl = 'http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles/barking%20and%20dagenham.pdf'

#scrapepdf('http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202013/bournemouth.pdf')


#The PDFs themselves are at these URLs
for2012 = 'http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles/'
for201314 = 'http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/'
#Each list of PDF names has been scraped using Outwit

pdflist12 = ['barnet.pdf','barnsley.pdf','bexley.pdf','bedford.pdf','birmingham.pdf','bolton.pdf','bracknell%20forest.pdf','blackburn%20with%20darwen.pdf','blackpool.pdf','bournemouth.pdf','bromley.pdf','bury.pdf','buckinghamshire.pdf','brent.pdf','bristol.pdf','brighton%20and%20hove.pdf','cheshire%20east.pdf','calderdale.pdf','central%20bedfordshire.pdf','cambridgeshire.pdf','camden.pdf','cheshire%20west%20and%20chester.pdf','coventry.pdf','city%20of%20london.pdf','croydon.pdf','cumbria.pdf','cornwall.pdf','darlington.pdf','derby.pdf','derbyshire.pdf','doncaster.pdf','dorset.pdf','devon.pdf','dudley.pdf','durham.pdf','essex.pdf','gateshead.pdf','east%20sussex.pdf','enfield.pdf','ealing.pdf','greenwich.pdf','gloucestershire.pdf','hackney.pdf','halton.pdf','hammersmith%20and%20fulham.pdf','hampshire.pdf','hertfordshire.pdf','haringey.pdf','herefordshire.pdf','hartlepool.pdf','harrow.pdf','havering.pdf','hillingdon.pdf','kent.pdf','kensington%20and%20chelsea.pdf','hounslow.pdf','isle%20of%20wight.pdf','islington.pdf','kingstonuponhull.pdf','kingstonuponthames.pdf','lancashire.pdf','lambeth.pdf','kirklees.pdf','knowsley.pdf','leeds.pdf','lewisham.pdf','leicester.pdf','leicestershire.pdf','liverpool.pdf','lincolnshire.pdf','luton.pdf','merton.pdf','manchester.pdf','medway.pdf','middlesbrough.pdf','milton%20keynes.pdf','newcastle%20upon%20tyne.pdf','newham.pdf','norfolk.pdf','north%20east%20lincolnshire.pdf','north%20lincolnshire.pdf','north%20somerset.pdf','north%20tyneside.pdf','north%20yorkshire.pdf','oldham.pdf','northamptonshire.pdf','northumberland.pdf','nottinghamshire.pdf','nottingham.pdf','oxfordshire.pdf','peterborough.pdf','redbridge.pdf','portsmouth.pdf','poole.pdf','plymouth.pdf','reading.pdf','redcar%20%20cleveland.pdf','richmonduponthames.pdf','rochdale.pdf','rutland.pdf','salford.pdf','sandwell.pdf','rotherham.pdf','sefton.pdf','sheffield.pdf','solihull.pdf','somerset.pdf','shropshire.pdf','slough.pdf','south%20gloucestershire.pdf','south%20tyneside.pdf','stockport.pdf','staffordshire.pdf','southwark.pdf','st%20helens.pdf','southampton.pdf','southendonsea.pdf','stocktonontees.pdf','stokeontrent.pdf','suffolk.pdf','sunderland.pdf','surrey.pdf','sutton.pdf','swindon.pdf','tameside.pdf','telford%20and%20wrekin.pdf','thurrock.pdf','torbay.pdf','tower%20hamlets.pdf','trafford.pdf','wakefield.pdf','walsall.pdf','waltham%20forest.pdf','wandsworth.pdf','warrington.pdf','warwickshire.pdf','west%20berkshire.pdf','west%20sussex.pdf','westminster.pdf','wigan.pdf','wiltshire.pdf','windsor%20and%20maidenhead.pdf','wirral.pdf','wolverhampton.pdf','worcestershire.pdf','york.pdf']
pdflist14 = ['bexley.pdf','bath-and-north-east-somerset.pdf','barking-and-dagenham.pdf','barnet.pdf','bedford.pdf','barnsley.pdf','bournemouth.pdf','bracknell-forest.pdf','brent.pdf','blackpool.pdf','blackburn-with-darwen.pdf','brighton-and-hove.pdf','bolton.pdf','bristol.pdf','bromley.pdf','bury.pdf','buckinghamshire.pdf','cheshire-east.pdf','cambridgeshire.pdf','calderdale.pdf','central-bedfordshire.pdf','cheshire-west-and-chester.pdf','camden.pdf','cornwall.pdf','coventry.pdf','croydon.pdf','darlington.pdf','cumbria.pdf','derby.pdf','devon.pdf','derbyshire.pdf','doncaster.pdf','durham.pdf','ealing.pdf','dudley.pdf','east-sussex.pdf','dorset.pdf','essex.pdf','gateshead.pdf','enfield.pdf','gloucestershire.pdf','greenwich.pdf','hammersmith-and-fulham.pdf','hackney.pdf','halton.pdf','hampshire.pdf','harrow.pdf','hartlepool.pdf','herefordshire.pdf','hillingdon.pdf','havering.pdf','hertfordshire.pdf','isle-of-wight.pdf','hounslow.pdf','islington.pdf','kent.pdf','kingston-upon-hull.pdf','kensington-and-chelsea.pdf','lambeth.pdf','lancashire.pdf','kingston-upon-thames.pdf','lewisham.pdf','leicester.pdf','lincolnshire.pdf','leeds.pdf','luton.pdf','leicestershire.pdf','medway.pdf','newcastle-upon-tyne.pdf','milton-keynes.pdf','merton.pdf','newham.pdf','northamptonshire.pdf','north-lincolnshire.pdf','north-somerset.pdf','north-east-lincolnshire.pdf','north-tyneside.pdf','northumberland.pdf','manchester.pdf','nottingham.pdf','north-yorkshire.pdf','nottinghamshire.pdf','oldham.pdf','oxfordshire.pdf','poole.pdf','portsmouth.pdf','redbridge.pdf','peterborough.pdf','plymouth.pdf','reading.pdf','richmond-upon-thames.pdf','redcar-and-cleveland.pdf','rochdale.pdf','salford.pdf','sandwell.pdf','sefton.pdf','sheffield.pdf','shropshire.pdf','somerset.pdf','slough.pdf','solihull.pdf','southampton.pdf','south-tyneside.pdf','southend-on-sea.pdf','south-gloucestershire.pdf','southwark.pdf','staffordshire.pdf','st-helens.pdf','stoke-on-trent.pdf','stockton-on-tees.pdf','stockport.pdf','sunderland.pdf','sutton.pdf','suffolk.pdf','surrey.pdf','swindon.pdf','torbay.pdf','tameside.pdf','tower-hamlets.pdf','telford-and-wrekin.pdf','thurrock.pdf','wandsworth.pdf','warrington.pdf','wakefield.pdf','walsall.pdf','waltham-forest.pdf','trafford.pdf','west-berkshire.pdf','westminster.pdf','warwickshire.pdf','wigan.pdf','west-sussex.pdf','wolverhampton.pdf','wiltshire.pdf','wirral.pdf','windsor-and-maidenhead.pdf','worcestershire.pdf','york.pdf']

testlist = ['http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles/city%20of%20london.pdf','http://www.cipfa.org/~/media/files/services/research and statistics/cipfastats library profiles/bath and north east somerset', 'http://www.cipfa.org/~/media/files/services/research and statistics/cipfastats library profiles/bedford']
testlist14 = [ 'http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/barnsley.pdf']
testbexley = ['http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/cheshire-east.pdf']
'''
for item in testbexley:
    print 'SCRAPING', item
    scrapepdf(item.replace(' ','%20'), 2014)

'''
errorlist = []
#Testing this group against the same TOP/LEFT positions
# URL 404 error - but works when put in browser
for item in pdflist12:
    print 'SCRAPING', for2012+item
    scrapepdf(for2012+item, 2012)
#This loop works
for item in pdflist14:
    print 'SCRAPING', for201314+item
    scrapepdf(for201314+item, 2014)
'''

for item in checklist:
    print 'SCRAPING', item
    if '%202014' in item:
        year = 2014
    else:
        year = 2012
    scrapepdf(item, year)

'''
