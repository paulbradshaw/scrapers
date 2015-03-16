#!/usr/bin/env python
import scraperwiki
import lxml.html
import urllib

#scrape table function
def scrape_table(root):
    rows = root.cssselect("table#AutoNumber2 tr")  # selects all <tr blocks in <table id="AutoNumber2"
    for row in rows[0:-2]:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.cssselect("td")
        if table_cells: 
            record['Rink'] = table_cells[0].text_content()
            record['Address'] = table_cells[1].text_content()
            print "len", len(table_cells[2].text_content())
            if len(table_cells[2].text_content())>0:
                record['Area'] = table_cells[2].text_content()
            record['County'] = table_cells[3].text_content()
            record['Phone'] = table_cells[4].text_content()
            showteamsurls = table_cells[5].cssselect('a')
            mapurls = table_cells[6].cssselect('a')
            if len(mapurls)>0:
                record['Maplink'] = mapurls[0].attrib.get('href')
            else:
                record['Maplink'] = "NO MAP LINK"
            if len(showteamsurls)>0:
                record['teamslink'] = showteamsurls[0].attrib.get('href')
            else:
                record['teamslink'] = "NO MAP LINK"
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.sql.save(["Rink"], record)


base_url = 'http://www.eiharec.co.uk/rink_list.php'
starting_url = base_url
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    #print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    

scrape_and_look_for_next_link(starting_url)



