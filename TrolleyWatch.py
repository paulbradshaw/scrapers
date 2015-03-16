#!/usr/bin/env python
import scraperwiki
import lxml.html

base_url = 'http://inmo.ie/6022'
starting_url = base_url
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    
def scrape_table(root):
    rows = root.cssselect("table.Trolley tr")  # selects all <tr blocks within <table class="data"
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.cssselect("td")
        if table_cells: 
            record['Date'] = table_cells[0].text
            record['Hospital'] = table_cells[1].text
            record['Region'] = table_cells[2].text
            record['Trolley total'] = table_cells[3].text
            record['Ward total'] = table_cells[4].text
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.sql.save(["Hospital"], record)

scrape_and_look_for_next_link(starting_url)



