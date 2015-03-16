#!/usr/bin/env python
import scraperwiki
import lxml.html
import urllib

#scrape table function
def scrape_table(root):
    rows = root.cssselect("tr")  # selects all <tr blocks
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.cssselect("td")
        if table_cells: 
            record['Course'] = table_cells[0].text_content()
            record['Address'] = table_cells[1].text_content()
            table_cellsurls = table_cells[2].cssselect('a')
            if len(table_cellsurls)>0:
                record['Maplink'] = table_cellsurls[0].attrib.get('href')
            else:
                record['Maplink'] = "NO MAP LINK"
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.sql.save(["Course"], record)


base_url = 'http://www.ukjockey.com/maps.html'
starting_url = base_url
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    #print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    

scrape_and_look_for_next_link(starting_url)



