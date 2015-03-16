import requests
import lxml.html

START_URL = 'https://jobsearch.direct.gov.uk/Reports/Reports.aspx?setype=1&seswitch=1'

# Set up a session
s = requests.session()

# Get a cookie by requesting the initial url
response = s.get(START_URL)

root = lxml.html.fromstring(response.text.encode('utf-8'))

# Capture the __VIEWSTATE in the form
VIEWSTATE = root.xpath('//input[@name="__VIEWSTATE"]')[0].attrib['value']

# Set up some headers (some of these might not be needed)
headers = {}
headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.149 Safari/537.36'
headers['Referer'] = 'https://jobsearch.direct.gov.uk/Reports/Reports.aspx?setype=1&seswitch=1'
headers['Origin'] = 'https://jobsearch.direct.gov.uk'
headers['Host'] = 'jobsearch.direct.gov.uk'
headers['Content-Length'] = 11485

# Set up the payload for the post request
payload = {}

# This is the first link ('Active jobs by industrial and occupational classification')
# You can get the __EVENTTARGET from the links id:
"""
<a id="MasterPage1_MainContent_folderControl_rptItems__ctl0_btnItem" href="javascript:__doPostBack('MasterPage1$MainContent$folderControl$rptItems$_ctl0$btnItem','')" tabindex="100">
                                    <!--<img alt='Report' src="http://media.newjobs.com/id/WebAdmin/reportwrapper/Report.png" style="width:24px;height:24px;vertical-align:middle;border:0" /> -->
                                    <span class="fnt24">
                                        Active jobs by industrial and occupational classification
                                    </span>
                                </a>
"""
payload['__EVENTTARGET'] = 'MasterPage1$MainContent$folderControl$rptItems$_ctl0$btnItem'
payload['__EVENTARGUMENT'] = ''
payload['__VIEWSTATE'] = VIEWSTATE
payload['__VIEWSTATEENCRYPTED'] = ''

# These control the default inputs in the forms search, they might be redundant
payload['MasterPage1:HeaderContent:Header_Default:searchControlsSwitcher:_ctl0:_tbKeywords'] ='Keywords (e.g. nurse)'
payload['MasterPage1:HeaderContent:Header_Default:searchControlsSwitcher:_ctl0:_ddlCountries'] ='160'
payload['MasterPage1:HeaderContent:Header_Default:searchControlsSwitcher:_ctl0:_tbWhere']= 'City, county or postcode'
payload['MasterPage1:HeaderContent:Header_Default:searchControlsSwitcher:_ctl0:defaultRadius']= '20'
payload['MasterPage1:HeaderContent:Header_Default:searchControlsSwitcher:_ctl0:_joblocations'] = ''
payload['MasterPage1:HeaderContent:Header_Default:searchControlsSwitcher:_ctl0:radiusUnits'] = ''

# Post away
response2 = s.post(START_URL, data=payload, headers=headers)

print response2.text.encode('utf-8')
