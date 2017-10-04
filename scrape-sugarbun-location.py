import mechanicalsoup as ms
from bs4 import BeautifulSoup
import pandas as pd

br = ms.StatefulBrowser(soup_config={'features': 'lxml'})

br.open('http://www.sugarbun.com/outlets')

page = br.get_current_page()

soup = BeautifulSoup(page.encode('utf-8'), 'html.parser')

states = soup.find_all('div', class_='state')


list_name = []
list_address = []
list_lat = []
list_lon = []
list_states = []

for state in states:
    statename = state.find('h1', text=True)
    districts = state.find_all('div', class_='district')
    for district in districts:
        name = list(district.find('h2'))[0]
        address = list(district.find('div', class_='add'))[0]
        getLatLon =district.find('a', class_='openmap')
        latlon = getLatLon['href']
        latlon = (latlon.split('@'))[1]
        lat = (latlon.split(','))[0]
        lon = (latlon.split(','))[1]
        list_name.append(name)
        list_address.append(address)
        list_lat.append(lat)
        list_lon.append(lon)
        list_states.append(statename)

df = pd.DataFrame()
df['name'] = list_name
df['address'] = list_address
df['latitude'] = list_lat
df['longitude'] = list_lon
df['states'] = list_states

df.to_csv('sugarbun-location.csv', index=False)
