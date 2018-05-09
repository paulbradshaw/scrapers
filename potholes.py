#!/usr/bin/env python
#Import our libraries that we need to grab the URLs and scrape them
import scraperwiki
import requests
import json
import urllib2
import scraperwiki
import lxml.etree

# URL 'names' scraped from http://streetrepairs.co.uk/councils/ using Outwit
# There's a map on each council page which pulls from JSON
# JSON is at similar URL http://streetrepairs.co.uk/councils/get_markers?council=lancashire-county-council . 
# So list of council names as used by site is then used to generate JSON URLs

#This is the list of council names as used within URLs, pasted from Excel as a *string*
councils = '''lancashire-county-council
derbyshire-county-council
northamptonshire-county-council
plymouth-city-council
staffordshire-county-council
surrey-county-council
essex-county-council
kent-county-council
highways-agency
blackburn-with-darwen-borough-council
buckinghamshire-county-council
oxfordshire-county-council
west-sussex-county-council
cornwall-council
hertfordshire-county-council
hampshire-county-council
devon-county-council
nottinghamshire-county-council
gloucestershire-county-council
east-sussex-county-council
lincolnshire-county-council
birmingham-city-council
cambridgeshire-county-council
north-somerset-council
sheffield-council
city-of-glasgow
cumbria-county-council
wiltshire-council
cheshire-east
manchester-city-council
norfolk-county-council
north-yorkshire-county-council
north-ayrshire-council
worcestershire-county-council
milton-keynes-council
london-borough-of-barnet
leicestershire-county-council
south-lanarkshire-council
highways-england
suffolk-county-council
durham-county-council
leeds-city-council
dumfries-and-galloway-council
falkirk-district-council
somerset-county-council
royal-borough-of-windsor-and-maidenhead
kirklees-metropolitan-borough-council
london-borough-of-lambeth
london-borough-of-brent
cheshire-west-and-chester
london-borough-of-bromley
cardiff-council
city-of-edinburgh
rossendale
london-borough-of-sutton
west-berkshire-council
central-bedfordshire-council
fife-council
oldham-metropolitan-borough-council
bolton-metropolitan-borough-council
liverpool-city-council
north-lanarkshire-council
east-ayrshire-council
salford-city-council
southampton-city-council
dundee-city-council
aberdeenshire
london-borough-of-croydon
london-borough-of-hounslow
trafford-council
bury-metropolitan-borough-council
dudley-metropolitan-borough
south-ayrshire-council
transport-scotland
nottingham-city-council
torbay-council
warwickshire-county-council
london-borough-of-ealing
peterborough-city-council
wirral-metropolitan-borough
isle-of-wight-council
south-gloucestershire-district-council
hull-city-council
northumberland-county-council
rochdale-metropolitan-borough-council
sefton-metropolitan-borough-council
coventry-city-council
dorset-county-council
renfrewshire-council
rotherham-metropolitan-borough-council
shropshire-council
perth-kinross-council
rutland-county-council
sandwell-metropolitan-borough-council
stoke-on-trent-city-council
tameside-metropolitan-borough-council
city-of-westminster
east-riding-of-yorkshire-council
london-borough-of-islington
reading-borough-council
derby-city-council
drdni-northern-division
herefordshire-council
london-borough-of-havering
scottish-borders-council
solihull-metropolitan-borough-council
swindon-borough-council
bournemouth-borough-council
bristol-city-council
calderdale
highland-council
leicester-city-council
london-borough-of-lewisham
luton-borough-council
north-tyneside-council
slough-borough-council
wigan-metropolitan-borough
bradford-metropolitan-council
denbighshire-council
doncaster-metropolitan-borough-council
london-borough-of-merton
stockport-metropolitan-borough-council
east-dunbartonshire-council
inverclyde-council
london-borough-of-greenwich
london-borough-of-hillingdon
midlothian-council
thurrock-council
bath-north-east-somerset-council
london-borough-of-wandsworth
aberdeen-city
london-borough-of-hammersmith-fulham
london-borough-of-southwark
royal-borough-of-kingston-upon-thames
wakefield-city-metropolitan-district-council
walsall-metropolitan-borough-council
wokingham-council
wolverhampton-city-council
argyll-bute-council
barnsley-borough-council
blaenau-gwent-county-borough
bridgend-county-borough-council
corby-borough-council
drdni-southern-division
flintshire-county-council
london-borough-of-bexley
medway-council
north-lincolnshire-council
south-northamptonshire
warrington-council
bedford-borough-council
city-county-of-swansea
gateshead-metropolitan-borough-council
london-borough-of-barking-dagenham
london-borough-of-hackney
london-borough-of-haringey
london-borough-of-harrow
royal-borough-of-kensington-chelsea
st-helens-borough-council
stirling-council
stockton-on-tees-borough-council
west-lothian-council
wrexham-county-borough-council
burnley-borough-council
canterbury-city-council
city-of-york
drdni-eastern-division
exeter-city
lancaster-city-council
newcastle-upon-tyne-city-council
newport-council
north-east-derbyshire
rhondda-cynon-taf-county-borough-council
sunderland-city-council
vale-of-glamorgan
blackpool-council
city-of-london-corporation
darlington-borough-council
east-renfrewshire-council
gloucester-city-council
harrogate-borough-council
london-borough-of-enfield
london-borough-of-redbridge
middlesbrough-borough-council
north-east-lincolnshire-council
portsmouth-city-council
spelthorne-borough-council
west-dunbartonshire
angus-council
basildon-district-council
brighton-and-hove-city-council
ceredigion-county-council
cheltenham-borough-council
erewash-borough
gwynedd-council
london-borough-of-newham
london-borough-of-tower-hamlets
london-borough-of-waltham-forest
pembrokeshire-council
selby
transport-for-london
ashfield-district-council
bracknell-forest-council
carmarthenshire-county-council
chesterfield-borough-council
epping-forest-district-council
hastings-borough-council
kings-lynn-and-west-norfolk-borough-council
merthyr-tydfil-council
oxford-city-council
poole-borough-council
south-tyneside-metropolitan-borough-council
west-lindsey
amber-valley-borough-council
carlisle-city-council
conwy-county-borough-council
eastbourne-council
fenland-district-council
fylde-borough-council
great-yarmouth-borough-council
high-peak-borough
isle-of-anglesey-council
knowsley-metropolitan-borough
lincoln-city-council
london-borough-of-camden
mid-sussex-district-council
neath-port-talbot-council
richmondshire
south-lakeland-district-council
south-staffordshire
swale-borough-council
telford-wrekin-council
winchester-city-council
adur-district-council
ashford-borough-council
aylesbury-vale-district-council
barrow-in-furness-borough-council
blaby-district-council
brentwood-borough-council
broxbourne-council
caerphilly-county-borough-council
cambridge-city-council
cannock-chase-district-council
charnwood-borough-council
chelmsford-borough-council
cherwell-district-council
crawley-borough-council
drdni-western-division
east-lindsey-district-council
east-lothian-council
east-northamptonshire-council
eden-district-council
wycombe-district-council
allerdale-borough-council
arun-district-council
babergh-district-council
basingstoke-deane-borough-council
bassetlaw-district-council
bolsover-district-council
boston-borough-council
braintree-district-council
breckland-district-council
broadland-district-council
bromsgrove-district-council
broxtowe-borough-council
castle-point
chichester-district-council
chiltern-district-council
chorley-borough-council
christchurch-borough-council
clackmannanshire-council
colchester-borough-council
comhairle-nan-eilean-siar-western-isles-council
copeland-borough-council
cotswold-district-council
council-of-the-isles-of-scilly
craven-district-council
dacorum-borough-council
dartford-borough-council
daventry-district-council
derbyshire-dales
dover-district-council
east-cambridgeshire
east-devon
east-dorset-district-council
east-hampshire-district-council
east-hertfordshire
eastleigh-borough-council
east-staffordshire-borough-council
epsom-ewell-borough-council
fareham-borough-council
forest-heath-district-council
forest-of-dean-district-council
gedling-borough-council
guildford-borough-council
hambleton
harborough-district-council
harlow-council
hart-district-council
hartlepool-borough-council
havant-district-council
hertsmere-borough-council
hinckley-bosworth-district-council
horsham-district-council
hyndburn-borough-council
ipswich-borough-council
kettering-borough-council
lewes-district-council
lichfield-district-council
maidstone-borough-council
maldon-district-council
malvern-hills-district-council
mansfield-district-council
melton-borough-council
mid-devon-district-council
mid-suffolk-district-council
mole-valley-council
newcastle-under-lyme-council
northampton-borough-council
north-devon-district-council
north-dorset-district-council
north-hertfordshire-district-council
north-norfolk-district-council
north-warwickshire-borough-council
north-west-leicestershire
norwich-city-council
nuneaton-bedworth
oadby-wigston-district-council
orkney-islands-council
pendle-borough-council
preston-city-council
purbeck-district-council
redcar-and-cleveland
redditch-borough-council
reigate-and-banstead-borough-council
ribble-valley-borough-council
rother-district-council
rushcliffe-council
ryedale-district-council
scarborough-borough-council
sedgemoor-district-council
sevenoaks-district-council
shepway-district-council
shetland-islands-council
south-bucks-district-council
south-cambridgeshire
southend-on-sea-council
south-hams-district-council
south-holland
south-kesteven
south-ribble-borough-council
south-somerset-district-council
staffordshire-moorlands-district-council
st-albans-city-district-council
st-edmundsbury-borough-council
stevenage-borough-council
stratford-on-avon
stroud-district-council
suffolk-coastal-district-council
surrey-heath-borough-council
tandridge-district-council
taunton-deane-borough-council
teignbridge-district-council
tendring-district-council
test-valley-borough-council
three-rivers-district-council
tonbridge-and-malling-borough-council
torfaen-county-borough
torridge-district-council
tunbridge-wells-borough-council
uttlesford-district-council
vale-of-white-horse-district-council
warwick-district-council
waverley-borough-council
wellingborough
welwyn-hatfield-council
west-devon-borough-council
west-dorset-district-council
west-lancashire-district-council
west-oxfordshire
west-somerset
weymouth-portland-borough-council
woking-borough-council
worthing-borough-council
wychavon-district-council
wyre-borough-council
wyre-forest-district-council'''

#That long string is split on each new line to create a list to loop through
councillist = councils.split('\n')
#Test by printing the 3rd to 4th items in the list
print councillist[2:4]
# This new string variable will be added to each council name in a mo
baseurl='http://streetrepairs.co.uk/councils/get_markers?council='
#Create an empty list, this will be filled with our new full URLs
jsonurls = []
#Loop through our list of council names
for council in councillist:
    #Add the baseurl string to them to form a full URL
    counciljson = 'http://streetrepairs.co.uk/councils/get_markers?council='+str(council)
    #Append that full URL to our previously empty list
    jsonurls.append(counciljson)

#Show how many items are in the list (its length)
print len(jsonurls)
#Test by printing items at index 2 to 4 in that list
print jsonurls[2:5]


html = requests.get("http://streetrepairs.co.uk/councils/get_markers?council=lancashire-county-council")
print html.content
#This is a string, beginning and ending with [], and with each JSON object in {}, separate by a comma
#This could be split on '{', or ',' or use the json library to store as a dict
jsonp = html.content[1:-1]
jsonlist = jsonp.split('},{')

