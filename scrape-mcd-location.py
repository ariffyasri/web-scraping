import mechanicalsoup as ms
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

page = open('mcd-location.html','r').read()

soup = BeautifulSoup(page, 'html.parser')

# print(soup.prettify())

addressBox = soup.find_all('div',class_='addressBox')

list_name = []
list_address = []
list_lat = []
list_lon = []

for each in addressBox:
    addressTop = each.find('div', class_='addressTop')
    addressBelow = each.find('div', class_='addressBelow')
    getName = addressTop.find('p', class_='addressTitle')
    getName = list(getName.find('strong'))[0]
    getAddress = list(addressTop.find('p', class_='addressText'))[0]


    getLatLon = list(addressBelow.find_all('a', class_='map_link_color'))[1]
    onClick = getLatLon['onclick']
    latlon = onClick[39:].split('&')
    lat = float((latlon[0].split(','))[0])
    lon = float((latlon[0].split(','))[1])
    list_name.append(getName)
    list_address.append(getAddress)
    list_lat.append(lat)
    list_lon.append(lon)

df = pd.DataFrame()
df['name'] = list_name
df['address'] = list_address
df['latitude'] = list_lat
df['longitude'] = list_lon

df.to_csv('mcd-location.csv', index=False)



