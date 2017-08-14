# reference : https://github.com/hickford/MechanicalSoup

import mechanicalsoup as ms
from bs4 import BeautifulSoup

# Browser
br = ms.StatefulBrowser(
	soup_config={'features': 'lxml'}
)
# open login page
br.open('https://www.linkedin.com/uas/login')

# search form tag
br.select_form('form')

# set credential
br["session_key"] = 'email'
br["session_password"] = 'password'

# submit the login form
resp = br.submit_selected()

# keyword 
keyword = 'data-analyst'
location = 'my'
# after login, open the
br.open('https://www.linkedin.com/jobs/search/?keywords='+keyword+'&locationId='+location)

# get the current page source code
page = br.get_current_page()

# do whatever you want such as print the source code
# directly extract any information you want or
# anything
print(page.encode('utf-8'))
