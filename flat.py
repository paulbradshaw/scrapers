
#Find region URLs

#Find links on regional browse page

regionurl = 'http://www.rightmove.co.uk/property-to-rent/Birmingham.html'

#grab any <a class = "propertyCard-link">
listinglinks = root.cssselect('a.propertyCard-link')

#this is div class="sect " - note the extra space before the end of the name. How to specify that? ('div.sect.')?
divsects = root.cssselect('div.sect')
record['description'] = divsects[0].text_content()
#Will we need to do a text analysis using R or SQL?
