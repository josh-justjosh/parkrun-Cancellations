import datetime
def now():
    return datetime.datetime.utcnow()
print(now(),'Script Start')

import requests
import json
import csv
from bs4 import BeautifulSoup
from html_table_extractor.extractor import Extractor
from html.parser import HTMLParser
import xml.etree.ElementTree as ET
import twython
import os
import collections

consumer_key = os.environ['consumer_key']
consumer_secret = os.environ['consumer_secret']
access_token = os.environ['access_token']
access_token_secret = os.environ['access_token_secret']

from twython import Twython
twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret)

def tweet(message):
    twitter.update_status(status=message)
    print("Tweeted: "+message)

def rem_dups(x):
    return list(dict.fromkeys(x))

old_cancellations_data = []
with open('_data/parkrun/cancellations.tsv','r', encoding='utf-8', newline='') as f:
    tsv_reader = csv.reader(f, delimiter="\t")
    for row in tsv_reader:
        row = rem_dups(row)
        old_cancellations_data.append(row)
print(now(),'cancellations.tsv read')
old_cancellations_data.remove(['Event','Country','Cancellation Note','Website'])

states_list = []
with open('_data/parkrun/raw/states.tsv','r', encoding='utf-8', newline='') as f:
    tsv_reader = csv.reader(f, delimiter="\t")
    for row in tsv_reader:
        states_list.append(row)
print(now(),'raw/states.tsv read')
states_list.remove(['Event','Country','State','County'])

def same_week(dateString):
    '''returns true if a dateString in %Y%m%d format is part of the current week'''
    d1 = datetime.datetime.strptime(dateString,'%Y-%m-%d')
    d2 = datetime.datetime.today()
    return d1.isocalendar()[1] == d2.isocalendar()[1] \
              and d1.year == d2.year  

events = requests.get('https://images.parkrun.com/events.json').text

with open('_data/parkrun/raw/events.json','wt', encoding='utf-8', newline='') as f:
    f.write(json.dumps(json.loads(events), indent=2))
    print(now(),"raw/events.json saved")

technical_event_info = requests.get('https://wiki.parkrun.com/index.php/Technical_Event_Information').text

#with open('_data/parkrun/raw/tei.html','wt', encoding='utf-8', newline='') as f:
#    f.write(technical_event_info)
#    print(now(),"raw/tei.html saved")

cancellations = requests.get('https://wiki.parkrun.com/index.php/Cancellations/Global').text

#with open('_data/parkrun/raw/cancellations.html','wt', encoding='utf-8', newline='') as f:
#    f.write(cancellations)
#    print(now(),"raw/cancellations.html saved")

events = json.loads(events)['events']

soup = BeautifulSoup(technical_event_info, 'html.parser')

extractor = Extractor(soup)
extractor.parse()
tei_table = extractor.return_list()
#print(now(),tei_table)

upcoming_events_table = []
upcoming_events = []

for i in tei_table:
    out = []
    for j in i:
        j = j.strip()
        out.append(j)
    #print(now(),out)
    if 'AcceptingRegistrations' in out:
        upcoming_events.append(out[0])
        upcoming_events_table.append(out)
#print(now(),upcoming_events)

    
soup = BeautifulSoup(cancellations, 'html.parser')

extractor = Extractor(soup)
extractor.parse()
cancellation_table = extractor.return_list()
cancellation_table.pop(-1)
cancellation_table.pop(0)

cancellations_data = []
cancellations_list = []

for i in range(len(cancellation_table)):
    try:
        for x in range(5):
            cancellation_table[i][x] = cancellation_table[i][x].strip()
    except IndexError:
        break
    
    if same_week(cancellation_table[i][0]) == True:
        #print(now(),cancellation_table[i])
        cancellations_data.append([cancellation_table[i][1],cancellation_table[i][3],cancellation_table[i][4]])
        cancellations_list.append(cancellation_table[i][1])

def sortByIndex0(e):
    return e[0]
def sortByIndex1(e):
    return e[1]

cancellation_table.sort(key=sortByIndex0)
cancellation_table.sort(key=sortByIndex1)

with open('_data/parkrun/all-cancellations.tsv','wt', encoding='utf-8', newline='') as f:
    tsv_writer = csv.writer(f, delimiter='\t')
    tsv_writer.writerow(['Date','Event','Region','Country','Cancellation Note'])
    for i in cancellation_table:
        tsv_writer.writerow(i)
    print(now(),"all-cancellations.tsv saved")

cancellation_dates = []
new_states_list = []

x = 0

#upcoming_events.append('Central parkrun, Plymouth')     #01/01/99   https://www.parkrun.org.uk/centralplymouth/
#upcoming_events.append('Church Mead parkrun')           #01/01/99   https://www.parkrun.org.uk/churchmead/
#upcoming_events.append('Edgbaston Reservoir parkrun')   #01/01/99   https://www.parkrun.org.uk/edgbastonreservoir/
#upcoming_events.append('Henlow Bridge Lakes parkrun')   #01/01/99   https://www.parkrun.org.uk/henlowbridgelakes/
#upcoming_events.append('Penryn Campus parkrun')         #01/01/99   https://www.parkrun.org.uk/penryncampus/
#upcoming_events.append('Roberts Park parkrun')          #01/01/99   https://www.parkrun.org.uk/robertspark/

for parkrun in events['features']:
    if parkrun['properties']['EventLongName'] in upcoming_events:
        #print(now(),parkrun)
        events['features'].remove(parkrun)

for parkrun in events['features']:
    #print(now(),parkrun['properties']['EventLongName'])
    if 'junior' in parkrun['properties']['EventLongName']:
        if parkrun['properties']['EventLongName'] in cancellations_list:
            parkrun['properties']['Status'] = 'junior Cancellation'
        else:
            parkrun['properties']['Status'] = 'junior parkrunning'
    else:
        if parkrun['properties']['EventLongName'] in cancellations_list:
            parkrun['properties']['Status'] = '5k Cancellation'
        else:
            parkrun['properties']['Status'] = 'parkrunning'

    for cancellation in cancellation_table:
        if parkrun['properties']['EventLongName'] == cancellation[1] and same_week(cancellation[0]) == True:
            parkrun['properties']['DateCancelled'] = cancellation[0]
            cancellation_dates.append(cancellation[0])
            parkrun['properties']['ReasonCancelled'] = cancellation[4]
            break
        else:
            parkrun['properties']['DateCancelled'] = None
            parkrun['properties']['ReasonCancelled'] = None

    if parkrun['properties']['countrycode'] == 3 :
        parkrun['properties']['Website'] = 'https://www.parkrun.com.au/'+parkrun['properties']['eventname']
        parkrun['properties']['Country'] = 'Australia'
    elif parkrun['properties']['countrycode'] == 4 :
        parkrun['properties']['Website'] = 'https://www.parkrun.co.at/'+parkrun['properties']['eventname']
        parkrun['properties']['Country'] = 'Austria'
    elif parkrun['properties']['countrycode'] == 14 :
        parkrun['properties']['Website'] = 'https://www.parkrun.ca/'+parkrun['properties']['eventname']
        parkrun['properties']['Country'] = 'Canada'
    elif parkrun['properties']['countrycode'] == 23 :
        parkrun['properties']['Website'] = 'https://www.parkrun.dk/'+parkrun['properties']['eventname']
        parkrun['properties']['Country'] = 'Denmark'
    elif parkrun['properties']['countrycode'] == 30 :
        parkrun['properties']['Website'] = 'https://www.parkrun.fi/'+parkrun['properties']['eventname']
        parkrun['properties']['Country'] = 'Finland'
    elif parkrun['properties']['countrycode'] == 31 :
        parkrun['properties']['Website'] = 'https://www.parkrun.fr/'+parkrun['properties']['eventname']
        parkrun['properties']['Country'] = 'France'
    elif parkrun['properties']['countrycode'] == 32 :
        parkrun['properties']['Website'] = 'https://www.parkrun.com.de/'+parkrun['properties']['eventname']
        parkrun['properties']['Country'] = 'Germany'
    elif parkrun['properties']['countrycode'] == 42 :
        parkrun['properties']['Website'] = 'https://www.parkrun.ie/'+parkrun['properties']['eventname']
        parkrun['properties']['Country'] = 'Ireland'
    elif parkrun['properties']['countrycode'] == 44 :
        parkrun['properties']['Website'] = 'https://www.parkrun.it/'+parkrun['properties']['eventname']
        parkrun['properties']['Country'] = 'Italy'
    elif parkrun['properties']['countrycode'] == 46 :
        parkrun['properties']['Website'] = 'https://www.parkrun.jp/'+parkrun['properties']['eventname']
        parkrun['properties']['Country'] = 'Japan'
    elif parkrun['properties']['countrycode'] == 57 :
        parkrun['properties']['Website'] = 'https://www.parkrun.my/'+parkrun['properties']['eventname']
        parkrun['properties']['Country'] = 'Malaysia'
    elif parkrun['properties']['countrycode'] == 65 :
        parkrun['properties']['Website'] = 'https://www.parkrun.co.nz/'+parkrun['properties']['eventname']
        parkrun['properties']['Country'] = 'New Zealand'
    elif parkrun['properties']['countrycode'] == 67 :
        parkrun['properties']['Website'] = 'https://www.parkrun.no/'+parkrun['properties']['eventname']
        parkrun['properties']['Country'] = 'Norway'
    elif parkrun['properties']['countrycode'] == 74 :
        parkrun['properties']['Website'] = 'https://www.parkrun.pl/'+parkrun['properties']['eventname']
        parkrun['properties']['Country'] = 'Poland'
    elif parkrun['properties']['countrycode'] == 79 :
        parkrun['properties']['Website'] = 'https://www.parkrun.ru/'+parkrun['properties']['eventname']
        parkrun['properties']['Country'] = 'Russia'
    elif parkrun['properties']['countrycode'] == 82 :
        parkrun['properties']['Website'] = 'https://www.parkrun.sg/'+parkrun['properties']['eventname']
        parkrun['properties']['Country'] = 'Singapore'
    elif parkrun['properties']['countrycode'] == 85 :
        parkrun['properties']['Website'] = 'https://www.parkrun.co.za/'+parkrun['properties']['eventname']
        if parkrun['properties']['EventLongName'] in ['Windhoek parkrun','Omeya parkrun','Swakopmund parkrun','Walvis Bay parkrun']:
            parkrun['properties']['Country'] = 'Namibia'
        elif parkrun['properties']['EventLongName'] in ['Mbabane parkrun']:
            parkrun['properties']['Country'] = 'Eswatini'
        else:
            parkrun['properties']['Country'] = 'South Africa'
    elif parkrun['properties']['countrycode'] == 88 :
        parkrun['properties']['Website'] = 'https://www.parkrun.se/'+parkrun['properties']['eventname']
        parkrun['properties']['Country'] = 'Sweden'
    elif parkrun['properties']['countrycode'] == 97 :
        parkrun['properties']['Website'] = 'https://www.parkrun.org.uk/'+parkrun['properties']['eventname']
        parkrun['properties']['Country'] = 'United Kingdom'
    elif parkrun['properties']['countrycode'] == 98 :
        parkrun['properties']['Website'] = 'https://www.parkrun.us/'+parkrun['properties']['eventname']
        parkrun['properties']['Country'] = 'USA'
    elif parkrun['properties']['countrycode'] == 64 :
        parkrun['properties']['Website'] = 'https://www.parkrun.co.nl/'+parkrun['properties']['eventname']
        parkrun['properties']['Country'] = 'Netherlands'
    else: parkrun['properties']['Website'] = 'Unavailable'

    new = True
    for event in states_list:
        if event[0] == parkrun['properties']['EventLongName']:
            #print(now(),parkrun['properties']['EventShortName'],'already saved state')
            new_states_list.append(event)
            parkrun['properties']['State'] = event[2]
            parkrun['properties']['County'] = event[3]
            new = False

    if new == True:
        #print(now(),parkrun['properties']['EventShortName'],'not saved state')
        GEONAME_USERNAME = '_josh_justjosh'
        url = "http://api.geonames.org/countrySubdivision?lat="+str(parkrun['geometry']['coordinates'][1])+"&lng="+str(parkrun['geometry']['coordinates'][0])+"&radius=1.5&maxRows=1&level=2&username="+GEONAME_USERNAME
        root = ET.fromstring(requests.get(url).text.strip())
        try:
            state = root.find('countrySubdivision').find('adminName1').text
        except:
            state = "-Unknown-"
            print(now(),parkrun['properties']['EventLongName'],"- State not Found -",url)
        try:
            county = root.find('countrySubdivision').find('adminName2').text
        except:
            county = "-Unknown-"
            print(now(),parkrun['properties']['EventLongName'],'- County not found -',url)
        parkrun['properties']['State'] = state
        parkrun['properties']['County'] = county
        add = [parkrun['properties']['EventLongName'],parkrun['properties']['Country'],state,county]
        new_states_list.append(add)
        
        
    parkrun['properties']['description']='<h4 style="margin: 0 0 8px;">'+parkrun['properties']['EventLongName']+'</h4><table><tr><th>Status:</th>'
    parkrun['properties']['description']+='<td>'+parkrun['properties']['Status']+'</td>'
    parkrun['properties']['description']+='</tr>'
    
    if parkrun['properties']['ReasonCancelled'] != None:
        parkrun['properties']['description']+='<tr><th>Cancellation Note:</th><td>'+parkrun['properties']['ReasonCancelled']+'</td>'
        parkrun['properties']['description']+='</tr>'
    
    if parkrun['properties']['Website'] != 'Unavailable':
        parkrun['properties']['description']+='<tr><th>Website:</th><td><a href="'+parkrun['properties']['Website']+'">'+parkrun['properties']['Website'].replace('https://www.','')+'</a></td></tr>'
    else: print(now(),parkrun['properties']['EventShortName'],'- Website   Not Generated')    
    parkrun['properties']['description']+='</table>'

    x += 1
    #print(now(),x,"/",len(events['features']),'-',parkrun['properties']['EventShortName'],"processed")
    #if x == 1750:
     #   break
    
with open('_data/parkrun/events.json','w', encoding='utf-8') as f:
    f.write(json.dumps(events, indent=2))
print(now(),'events.json saved')

cancellation_dates = list(dict.fromkeys(cancellation_dates))
cancellation_dates.sort()
with open('_data/parkrun/cancellation-dates.tsv','wt', encoding='utf-8', newline='') as f:
    tsv_writer = csv.writer(f, delimiter='\t')
    for date in cancellation_dates:
        tsv_writer.writerow([date])
print(now(),"cancellation-dates.tsv saved")

events_data  = []
for event in events['features']:
    out = []
    out.append(event['properties']['EventLongName'])
    out.append(event['geometry']['coordinates'][1])
    out.append(event['geometry']['coordinates'][0])
    out.append(event['properties']['Country'])
    out.append(event['properties']['State'])
    out.append(event['properties']['County'])
    out.append(event['properties']['Status'])
    out.append(event['properties']['DateCancelled'])
    out.append(event['properties']['ReasonCancelled'])
    out.append(event['properties']['Website'])
    events_data.append(out)
events_data.sort()

with open('_data/parkrun/events-table.tsv','wt', encoding='utf-8', newline='') as f:
    tsv_writer = csv.writer(f, delimiter='\t')
    tsv_writer.writerow(['Event','Latitude','Longitude','Country','State','County','Status','Date Cancelled','Reason Cancelled','Website'])
    for event in events_data:
        tsv_writer.writerow(event)
print(now(),"events-table.tsv saved")

countries = {
    'Australia': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    'Austria': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    'Canada': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    'Denmark': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    'Eswatini': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    'Finland': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    'France': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    'Germany': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    'Ireland': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    'Italy': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    'Japan': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    'Malaysia': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    'Namibia': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    'Netherlands': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    'New Zealand': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    'Norway': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    'Poland': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    'Russia': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    'Singapore': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    'South Africa': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    'Sweden': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    'United Kingdom': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    'USA': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    'Total': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    }

totals= {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        }
        

for parkrun in events['features']:
    if parkrun['properties']['Status'] == 'parkrunning':
        countries[parkrun['properties']['Country']]['parkrunning'] += 1
        countries[parkrun['properties']['Country']]['Total'] += 1
    elif parkrun['properties']['Status'] == 'junior parkrunning':
        countries[parkrun['properties']['Country']]['junior parkrunning'] += 1
        countries[parkrun['properties']['Country']]['Total'] += 1
    elif parkrun['properties']['Status'] == '5k Cancellation':
        countries[parkrun['properties']['Country']]['5k Cancellations'] += 1
        countries[parkrun['properties']['Country']]['Total'] += 1
    elif parkrun['properties']['Status'] == 'junior Cancellation':
        countries[parkrun['properties']['Country']]['junior Cancellations'] += 1
        countries[parkrun['properties']['Country']]['Total'] += 1
    elif parkrun['properties']['Status'] == 'PtR':
        countries[parkrun['properties']['Country']]['5k Cancellations'] += 1
        countries[parkrun['properties']['Country']]['Total'] += 1
    else:
        print(now(),"Error:",parkrun['properties']['EventLongName'])
#print(now(),countries)

for country,data in countries.items():
    totals['parkrunning'] += data['parkrunning']
    totals['junior parkrunning'] += data['junior parkrunning']
    totals['5k Cancellations'] += data['5k Cancellations']
    totals['junior Cancellations'] += data['junior Cancellations']
    totals['Total'] += data['Total']

countries['Total'] = totals

with open('_data/parkrun/countries-data.tsv','wt', encoding='utf-8', newline='') as f:
    tsv_writer = csv.writer(f, delimiter='\t')
    tsv_writer.writerow(['Country','parkrunning','junior parkrunning','5k Cancellations','junior Cancellations','Total'])
    for i,j in countries.items():
        out = [i]
        for k,l in j.items():
            if l != 0:
                out.append(l)
            else:
                out.append('')
        tsv_writer.writerow(out)
print(now(),"countries-data.tsv saved")

uk = {
    'England': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    'Northern Ireland': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    'Scotland': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    'Wales': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    'Other': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    'Total': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    }

uk_totals= {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        }

for parkrun in events['features']:
    if parkrun['properties']['Country'] == "United Kingdom":
        if parkrun['properties']['State'] in ['England','Northern Ireland','Scotland','Wales']:
            if parkrun['properties']['Status'] == 'parkrunning':
                uk[parkrun['properties']['State']]['parkrunning'] += 1
                uk[parkrun['properties']['State']]['Total'] += 1
            elif parkrun['properties']['Status'] == 'junior parkrunning':
                uk[parkrun['properties']['State']]['junior parkrunning'] += 1
                uk[parkrun['properties']['State']]['Total'] += 1
            elif parkrun['properties']['Status'] == '5k Cancellation':
                uk[parkrun['properties']['State']]['5k Cancellations'] += 1
                uk[parkrun['properties']['State']]['Total'] += 1
            elif parkrun['properties']['Status'] == 'junior Cancellation':
                uk[parkrun['properties']['State']]['junior Cancellations'] += 1
                uk[parkrun['properties']['State']]['Total'] += 1
            elif parkrun['properties']['Status'] == 'PtR':
                uk[parkrun['properties']['State']]['5k Cancellations'] += 1
                uk[parkrun['properties']['State']]['Total'] += 1
        else:
            if parkrun['properties']['Status'] == 'parkrunning':
                uk['Other']['parkrunning'] += 1
                uk['Other']['Total'] += 1
            elif parkrun['properties']['Status'] == 'junior parkrunning':
                uk['Other']['junior parkrunning'] += 1
                uk['Other']['Total'] += 1
            elif parkrun['properties']['Status'] == '5k Cancellation':
                uk['Other']['5k Cancellations'] += 1
                uk['Other']['Total'] += 1
            elif parkrun['properties']['Status'] == 'junior Cancellation':
                uk['Other']['junior Cancellations'] += 1
                uk['Other']['Total'] += 1
            elif parkrun['properties']['Status'] == 'PtR':
                uk['Other']['5k Cancellations'] += 1
                uk['Other']['Total'] += 1
            
#print(now(),countries)

for state,data in uk.items():
    uk_totals['parkrunning'] += data['parkrunning']
    uk_totals['junior parkrunning'] += data['junior parkrunning']
    uk_totals['5k Cancellations'] += data['5k Cancellations']
    uk_totals['junior Cancellations'] += data['junior Cancellations']
    uk_totals['Total'] += data['Total']

uk['Total'] = uk_totals

with open('_data/parkrun/uk-data.tsv','wt', encoding='utf-8', newline='') as f:
    tsv_writer = csv.writer(f, delimiter='\t')
    tsv_writer.writerow(['Country','parkrunning','junior parkrunning','5k Cancellations','junior Cancellations','Total'])
    for i,j in uk.items():
        out = [i]
        for k,l in j.items():
            if l != 0:
                out.append(l)
            else:
                out.append('')
        tsv_writer.writerow(out)
print(now(),"uk-data.tsv saved")

aus = {
    'Australian Capital Territory': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    'New South Wales': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    'Northern Territory': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    'Queensland': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    'South Australia': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    'Tasmania': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    'Victoria': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    'Western Australia': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    'Total': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        },
    }

aus_totals= {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Total':0
        }

for parkrun in events['features']:
    if parkrun['properties']['Country'] == "Australia":
        if parkrun['properties']['State'] in ['Queensland','New South Wales','Victoria','Australian Capital Territory','Western Australia','Tasmania','South Australia','Northern Territory']:
            if parkrun['properties']['Status'] == 'parkrunning':
                aus[parkrun['properties']['State']]['parkrunning'] += 1
                aus[parkrun['properties']['State']]['Total'] += 1
            elif parkrun['properties']['Status'] == 'junior parkrunning':
                aus[parkrun['properties']['State']]['junior parkrunning'] += 1
                aus[parkrun['properties']['State']]['Total'] += 1
            elif parkrun['properties']['Status'] == '5k Cancellation':
                aus[parkrun['properties']['State']]['5k Cancellations'] += 1
                aus[parkrun['properties']['State']]['Total'] += 1
            elif parkrun['properties']['Status'] == 'junior Cancellation':
                aus[parkrun['properties']['State']]['junior Cancellations'] += 1
                aus[parkrun['properties']['State']]['Total'] += 1
            elif parkrun['properties']['Status'] == 'PtR':
                aus[parkrun['properties']['State']]['5k Cancellations'] += 1
                aus[parkrun['properties']['State']]['Total'] += 1
        else:
            print(now(),parkrun['properties']['EventLongName'],"in Australia but not in state")

#print(now(),countries)

for state,data in aus.items():
    aus_totals['parkrunning'] += data['parkrunning']
    aus_totals['junior parkrunning'] += data['junior parkrunning']
    aus_totals['5k Cancellations'] += data['5k Cancellations']
    aus_totals['junior Cancellations'] += data['junior Cancellations']
    aus_totals['Total'] += data['Total']

aus['Total'] = aus_totals

with open('_data/parkrun/aus-data.tsv','wt', encoding='utf-8', newline='') as f:
    tsv_writer = csv.writer(f, delimiter='\t')
    tsv_writer.writerow(['Country','parkrunning','junior parkrunning','5k Cancellations','junior Cancellations','Total'])
    for i,j in aus.items():
        out = [i]
        for k,l in j.items():
            if l != 0:
                out.append(l)
            else:
                out.append('')
        tsv_writer.writerow(out)
print(now(),"aus-data.tsv saved")

uk_ie_counties = {}
for parkrun in events['features']:
    if parkrun['properties']['Country'] in ["United Kingdom", "Ireland"]:
        if parkrun['properties']['County'] not in ['', 'Douglas']:
            #England
            if parkrun['properties']['County'] in ['Bedford','Central Bedfordshire','Luton']:
                parkrun['properties']['County'] = 'Bedfordshire'
            elif parkrun['properties']['County'] in ['Bracknell Forest','Reading','Slough','West Berkshire','Windsor and Maidenhead','Wokingham']:
                parkrun['properties']['County'] = 'Berkshire'
            elif parkrun['properties']['County'] in ['Buckinghamshire','Milton Keynes']:
                parkrun['properties']['County'] = 'Buckinghamshire'
            elif parkrun['properties']['County'] in ['Cambridgeshire','Peterborough']:
                parkrun['properties']['County'] = 'Cambridgeshire'
            elif parkrun['properties']['County'] in ['Cheshire East','Cheshire','Halton','Warrington']:
                parkrun['properties']['County'] = 'Cheshire'
            elif parkrun['properties']['County'] in ['Derbyshire','Derby']:
                parkrun['properties']['County'] = 'Derbyshire'
            elif parkrun['properties']['County'] in ['Devon','Plymouth','Torbay']:
                parkrun['properties']['County'] = 'Devon'
            elif parkrun['properties']['County'] in ['Dorset','Bournemouth, Christchurch and Poole Council']:
                parkrun['properties']['County'] = 'Dorset'
            elif parkrun['properties']['County'] in ['Durham','Darlington','Hartlepool']:
                parkrun['properties']['County'] = 'Durham'
            elif parkrun['properties']['EventLongName'] in ['Tees Barrage parkrun','Billingham junior parkrun']:
                parkrun['properties']['County'] = 'Durham'
            elif parkrun['properties']['County'] in ['East Yorkshire','Kingston upon Hull']:
                parkrun['properties']['County'] = 'East Yorkshire'
            elif parkrun['properties']['County'] in ['East Sussex','Brighton and Hove']:
                parkrun['properties']['County'] = 'East Sussex'
            elif parkrun['properties']['County'] in ['Essex','Southend-on-Sea','Thurrock']:
                parkrun['properties']['County'] = 'Essex'
            elif parkrun['properties']['County'] in ['Gloucestershire','South Gloucestershire']:
                parkrun['properties']['County'] = 'Gloucestershire'
            #elif parkrun['properties']['County'] in ['City of Westminster', 'Kensington and Chelsea', 'Hammersmith and Fulham', 'Wandsworth', 'Lambeth', 'Southwark', 'Tower Hamlets', 'Hackney', 'Islington', 'Camden', 'Brent', 'Ealing', 'Hounslow', 'Richmond upon Thames', 'Kingston upon Thames', 'Merton', 'Sutton', 'Croydon', 'Bromley', 'Lewisham', 'Greenwich', 'Bexley', 'Havering', 'Barking and Dagenham', 'Redbridge', 'Newham', 'Waltham Forest', 'Haringey', 'Enfield', 'Barnet', 'Harrow', 'Hillingdon']:
                #parkrun['properties']['County'] = 'Greater London'
                #pass
            elif parkrun['properties']['County'] in ['Manchester','Bolton','Stockport','Tameside','Oldham','Rochdale','Bury','Bolton','Wigan','Salford','Trafford']:
                parkrun['properties']['County'] = 'Greater Manchester'
            elif parkrun['properties']['County'] in ['Liverpool','Wirral','Knowsley','Sefton','St. Helens']:
                parkrun['properties']['County'] = 'Merseyside'
            elif parkrun['properties']['County'] in ['Hampshire','Portsmouth','Southampton']:
                parkrun['properties']['County'] = 'Hampshire'
            elif parkrun['properties']['County'] in ['Kent','Medway']:
                parkrun['properties']['County'] = 'Kent'
            elif parkrun['properties']['County'] in ['Blackburn with Darwen','Blackpool','Lancashire']:
                parkrun['properties']['County'] = 'Lancashire'
            elif parkrun['properties']['County'] in ['Leicestershire','Leicester']:
                parkrun['properties']['County'] = 'Leicestershire'
            elif parkrun['properties']['County'] in ['Lincolnshire','North Lincolnshire','North East Lincolnshire']:
                parkrun['properties']['County'] = 'Lincolnshire'
            elif parkrun['properties']['County'] in ['Middlesbrough','North Yorkshire','Redcar and Cleveland','York']:
                parkrun['properties']['County'] = 'North Yorkshire'
            elif parkrun['properties']['County'] in ['Nottinghamshire','Nottingham']:
                parkrun['properties']['County'] = 'Nottinghamshire'
            elif parkrun['properties']['County'] in ['Shropshire','Telford and Wrekin']:
                parkrun['properties']['County'] = 'Shropshire'
            elif parkrun['properties']['County'] in ['Bath and North East Somerset','North Somerset','Somerset']:
                parkrun['properties']['County'] = 'Somerset'
            elif parkrun['properties']['County'] in ['Barnsley','Doncaster','Rotherham','Sheffield']:
                parkrun['properties']['County'] = 'South Yorkshire'
            elif parkrun['properties']['County'] in ['Staffordshire','Stoke-on-Trent']:
                parkrun['properties']['County'] = 'Staffordshire'
            elif parkrun['properties']['County'] in ['Gateshead','Newcastle upon Tyne','North Tyneside','South Tyneside','Sunderland']:
                parkrun['properties']['County'] = 'Tyne and Wear'
            elif parkrun['properties']['County'] in ['Birmingham','Wolverhampton','Dudley','Walsall','Sandwell','Solihull','Coventry']:
                parkrun['properties']['County'] = 'West Midlands'
            elif parkrun['properties']['County'] in ['Leeds','Wakefield','Kirklees','Calderdale','Bradford']:
                parkrun['properties']['County'] = 'West Yorkshire'
            elif parkrun['properties']['County'] in ['Swindon','Wiltshire']:
                parkrun['properties']['County'] = 'Wiltshire'
            #Wales
            elif parkrun['properties']['County'] in ['Conwy','Denbighshire','Flintshire','Wrexham']:
                parkrun['properties']['County'] = 'Clwyd'
            elif parkrun['properties']['County'] in ['Carmarthenshire','Ceredigion','Pembrokeshire']:
                parkrun['properties']['County'] = 'Dyfed'
            elif parkrun['properties']['County'] in ['Blaenau Gwent','Caerphilly','Monmouthshire','Newport','Torfaen County Borough']:
                parkrun['properties']['County'] = 'Gwent'
            elif parkrun['properties']['County'] in ['Gwynedd','Anglesey']:
                parkrun['properties']['County'] = 'Gwynedd'
            elif parkrun['properties']['County'] in ['County Borough of Bridgend','Merthyr Tydfil','Rhondda Cynon Taf']:
                parkrun['properties']['County'] = 'Mid Glamorgan'
            elif parkrun['properties']['County'] in ['Cardiff','Vale of Glamorgan']:
                parkrun['properties']['County'] = 'South Glamorgan'
            elif parkrun['properties']['County'] in ['Neath Port Talbot','City and County of Swansea']:
                parkrun['properties']['County'] = 'West Glamorgan'
                
            if parkrun['properties']['County'] not in uk_ie_counties:
                if parkrun['properties']['State'] in ['England','Northern Ireland','Scotland','Wales']:
                    uk_ie_counties[parkrun['properties']['County']] = {'country': parkrun['properties']['State'],'parkrunning': 0,'junior parkrunning':0,'5k Cancellations':0,'junior Cancellations':0,'Total':0,'events parkrunning':'','events junior parkrunning':'','events 5k cancellation':'','events junior cancellation':''}
                else:
                    uk_ie_counties[parkrun['properties']['County']] = {'country': parkrun['properties']['Country'],'parkrunning': 0,'junior parkrunning':0,'5k Cancellations':0,'junior Cancellations':0,'Total':0,'events parkrunning':'','events junior parkrunning':'','events 5k cancellation':'','events junior cancellation':''}
            if parkrun['properties']['Status'] == 'parkrunning':
                uk_ie_counties[parkrun['properties']['County']]['parkrunning'] += 1
                uk_ie_counties[parkrun['properties']['County']]['Total'] += 1
                uk_ie_counties[parkrun['properties']['County']]['events parkrunning'] += parkrun['properties']['EventShortName'] + '|'
            elif parkrun['properties']['Status'] == 'junior parkrunning':
                uk_ie_counties[parkrun['properties']['County']]['junior parkrunning'] += 1
                uk_ie_counties[parkrun['properties']['County']]['Total'] += 1
                uk_ie_counties[parkrun['properties']['County']]['events junior parkrunning'] += parkrun['properties']['EventShortName'] + '|'
            elif parkrun['properties']['Status'] == '5k Cancellation':
                uk_ie_counties[parkrun['properties']['County']]['5k Cancellations'] += 1
                uk_ie_counties[parkrun['properties']['County']]['Total'] += 1
                uk_ie_counties[parkrun['properties']['County']]['events 5k cancellation'] += parkrun['properties']['EventShortName'] + '|'
            elif parkrun['properties']['Status'] == 'junior Cancellation':
                uk_ie_counties[parkrun['properties']['County']]['junior Cancellations'] += 1
                uk_ie_counties[parkrun['properties']['County']]['Total'] += 1
                uk_ie_counties[parkrun['properties']['County']]['events junior cancellation'] += parkrun['properties']['EventShortName'] + '|'

uk_ie_counties_od = collections.OrderedDict(sorted(uk_ie_counties.items()))
uk_ie_counties = {}
for k, v in uk_ie_counties_od.items():
    uk_ie_counties[k] = v

uk_ie_counties_totals= {
    'country':'',
    'parkrunning': 0,
    'junior parkrunning':0,
    '5k Cancellations':0,
    'junior Cancellations':0,
    'Total':0
    }
england_totals= {
    'country':'England',
    'parkrunning': 0,
    'junior parkrunning':0,
    '5k Cancellations':0,
    'junior Cancellations':0,
    'Total':0
    }
ni_totals= {
    'country':'Northern Ireland',
    'parkrunning': 0,
    'junior parkrunning':0,
    '5k Cancellations':0,
    'junior Cancellations':0,
    'Total':0
    }
scotland_totals= {
    'country':'Scotland',
    'parkrunning': 0,
    'junior parkrunning':0,
    '5k Cancellations':0,
    'junior Cancellations':0,
    'Total':0
    }
wales_totals= {
    'country':'Wales',
    'parkrunning': 0,
    'junior parkrunning':0,
    '5k Cancellations':0,
    'junior Cancellations':0,
    'Total':0
    }
ireland_totals= {
    'country':'Ireland',
    'parkrunning': 0,
    'junior parkrunning':0,
    '5k Cancellations':0,
    'junior Cancellations':0,
    'Total':0
    }

for county,data in uk_ie_counties.items():
    uk_ie_counties_totals['parkrunning'] += data['parkrunning']
    uk_ie_counties_totals['junior parkrunning'] += data['junior parkrunning']
    uk_ie_counties_totals['5k Cancellations'] += data['5k Cancellations']
    uk_ie_counties_totals['junior Cancellations'] += data['junior Cancellations']
    uk_ie_counties_totals['Total'] += data['Total']
    if data['country'] == 'England':
        england_totals['parkrunning'] += data['parkrunning']
        england_totals['junior parkrunning'] += data['junior parkrunning']
        england_totals['5k Cancellations'] += data['5k Cancellations']
        england_totals['junior Cancellations'] += data['junior Cancellations']
        england_totals['Total'] += data['Total']
    if data['country'] == 'Northern Ireland':
        ni_totals['parkrunning'] += data['parkrunning']
        ni_totals['junior parkrunning'] += data['junior parkrunning']
        ni_totals['5k Cancellations'] += data['5k Cancellations']
        ni_totals['junior Cancellations'] += data['junior Cancellations']
        ni_totals['Total'] += data['Total']
    if data['country'] == 'Scotland':
        scotland_totals['parkrunning'] += data['parkrunning']
        scotland_totals['junior parkrunning'] += data['junior parkrunning']
        scotland_totals['5k Cancellations'] += data['5k Cancellations']
        scotland_totals['junior Cancellations'] += data['junior Cancellations']
        scotland_totals['Total'] += data['Total']
    if data['country'] == 'Wales':
        wales_totals['parkrunning'] += data['parkrunning']
        wales_totals['junior parkrunning'] += data['junior parkrunning']
        wales_totals['5k Cancellations'] += data['5k Cancellations']
        wales_totals['junior Cancellations'] += data['junior Cancellations']
        wales_totals['Total'] += data['Total']
    if data['country'] == 'Ireland':
        ireland_totals['parkrunning'] += data['parkrunning']
        ireland_totals['junior parkrunning'] += data['junior parkrunning']
        ireland_totals['5k Cancellations'] += data['5k Cancellations']
        ireland_totals['junior Cancellations'] += data['junior Cancellations']
        ireland_totals['Total'] += data['Total']

uk_ie_counties['England Total'] = england_totals
uk_ie_counties['NI Total'] = ni_totals
uk_ie_counties['Scotland Total'] = scotland_totals
uk_ie_counties['Wales Total'] = wales_totals
uk_ie_counties['Ireland Total'] = ireland_totals
uk_ie_counties['Total'] = uk_ie_counties_totals        
#print(json.dumps(uk_ie_counties, indent=4))

with open('_data/parkrun/counties/england.tsv','wt', encoding='utf-8', newline='') as f:
    tsv_writer = csv.writer(f, delimiter='\t')
    tsv_writer.writerow(['County','parkrunning','junior parkrunning','5k Cancellations','junior Cancellations','Total','5k Events Running','junior Events Running','5k Events Cancelled','junior Events Cancelled'])
    for i,j in uk_ie_counties.items():
        if j['country'] == 'England':
            if i == 'England Total':
                out = ['Total']
            else:
                out = [i]
            for k,l in j.items():
                if l == 'England':
                    pass
                elif l not in [0,[]]:
                    out.append(l)
                else:
                    out.append('')
            if i == 'England Total':
                for x in range(4):
                    out.append('')
            tsv_writer.writerow(out)
print(now(),"counties/england.tsv saved")

with open('_data/parkrun/counties/ni.tsv','wt', encoding='utf-8', newline='') as f:
    tsv_writer = csv.writer(f, delimiter='\t')
    tsv_writer.writerow(['County','parkrunning','junior parkrunning','5k Cancellations','junior Cancellations','Total','5k Events Running','junior Events Running','5k Events Cancelled','junior Events Cancelled'])
    for i,j in uk_ie_counties.items():
        if j['country'] == 'Northern Ireland':
            if i == 'NI Total':
                out = ['Total']
            else:
                out = [i]
            for k,l in j.items():
                if l == 'Northern Ireland':
                    pass
                elif l not in [0,[]]:
                    out.append(l)
                else:
                    out.append('')
            if i == 'NI Total':
                for x in range(4):
                    out.append('')
            tsv_writer.writerow(out)
print(now(),"counties/ni.tsv saved")

with open('_data/parkrun/counties/scotland.tsv','wt', encoding='utf-8', newline='') as f:
    tsv_writer = csv.writer(f, delimiter='\t')
    tsv_writer.writerow(['County','parkrunning','junior parkrunning','5k Cancellations','junior Cancellations','Total','5k Events Running','junior Events Running','5k Events Cancelled','junior Events Cancelled'])
    for i,j in uk_ie_counties.items():
        if j['country'] == 'Scotland':
            if i == 'Scotland Total':
                out = ['Total']
            else:
                out = [i]
            for k,l in j.items():
                if l == 'Scotland':
                    pass
                elif l not in [0,[]]:
                    out.append(l)
                else:
                    out.append('')
            if i == 'Scotland Total':
                for x in range(4):
                    out.append('')
            tsv_writer.writerow(out)
print(now(),"counties/scotalnd.tsv saved")

with open('_data/parkrun/counties/wales.tsv','wt', encoding='utf-8', newline='') as f:
    tsv_writer = csv.writer(f, delimiter='\t')
    tsv_writer.writerow(['County','parkrunning','junior parkrunning','5k Cancellations','junior Cancellations','Total','5k Events Running','junior Events Running','5k Events Cancelled','junior Events Cancelled'])
    for i,j in uk_ie_counties.items():
        if j['country'] == 'Wales':
            if i == 'Wales Total':
                out = ['Total']
            else:
                out = [i]
            for k,l in j.items():
                if l == 'Wales':
                    pass
                elif l not in [0,[]]:
                    out.append(l)
                else:
                    out.append('')
            if i == 'Wales Total':
                for x in range(4):
                    out.append('')
            tsv_writer.writerow(out)
print(now(),"counties/wales.tsv saved")

with open('_data/parkrun/counties/ireland.tsv','wt', encoding='utf-8', newline='') as f:
    tsv_writer = csv.writer(f, delimiter='\t')
    tsv_writer.writerow(['County','parkrunning','junior parkrunning','5k Cancellations','junior Cancellations','Total','5k Events Running','junior Events Running','5k Events Cancelled','junior Events Cancelled'])
    for i,j in uk_ie_counties.items():
        if j['country'] == 'Ireland':
            if i == 'Ireland Total':
                out = ['Total']
            else:
                out = [i]
            for k,l in j.items():
                if l == 'Ireland':
                    pass
                elif l not in [0,[]]:
                    out.append(l)
                else:
                    out.append('')
            if i == 'Ireland Total':
                for x in range(4):
                    out.append('')
            tsv_writer.writerow(out)
print(now(),"counties/ireland.tsv saved")

with open('_data/parkrun/counties/all.tsv','wt', encoding='utf-8', newline='') as f:
    tsv_writer = csv.writer(f, delimiter='\t')
    tsv_writer.writerow(['County','Country','parkrunning','junior parkrunning','5k Cancellations','junior Cancellations','Total','5k Events Running','junior Events Running','5k Events Cancelled','junior Events Cancelled'])
    for i,j in uk_ie_counties.items():
        out = [i]
        for k,l in j.items():
            if l not in [0,[]] :
                out.append(l)
            else:
                out.append('')
        if 'Total' in i:
            for x in range(4):
                out.append('')
        tsv_writer.writerow(out)
print(now(),"counties/all.tsv saved")

cancellations_changes = []
cancellations_additions = []
cancellations_removals = []

for i in old_cancellations_data:
    oldwebsite = i[3]
    i.pop(3)
    if i not in cancellations_data:
        #i.append('Removed')
        out = i
        for parkrun in events['features']:
            if parkrun['properties']['EventLongName'] == i[0]:
                out.append(oldwebsite)
                break
        cancellations_removals.append(out)

for i in cancellations_data:
    if i not in old_cancellations_data:
        #i.append('Added')
        out = i
        for parkrun in events['features']:
            if parkrun['properties']['EventLongName'] == i[0]:
                out.append(parkrun['properties']['Website'])
                break
        cancellations_additions.append(out)

for cancellation in cancellations_data:
    if len(cancellation) <= 3:
        out = ''
        for parkrun in events['features']:
            if parkrun['properties']['EventLongName'] == cancellation[0]:
                out = parkrun['properties']['Website']
                break
        cancellation.append(out)
        cancellation = rem_dups(cancellation)
        #print(now(),cancellation)

#print(now(),cancellations_changes)
cancellations_additions.sort()
cancellations_removals.sort()
cancellations_data.sort()

with open('_data/parkrun/cancellations.tsv','wt', encoding='utf-8', newline='') as f:
    tsv_writer = csv.writer(f, delimiter='\t')
    tsv_writer.writerow(['Event','Country','Cancellation Note','Website'])
    for event in cancellations_data:
        tsv_writer.writerow(event)
print(now(),"cancellations.tsv saved")

if cancellations_additions != []:
    with open('_data/parkrun/cancellation-additions.tsv','wt', encoding='utf-8', newline='') as f:
        tsv_writer = csv.writer(f, delimiter='\t')
        tsv_writer.writerow(['Event','Country','Cancellation Note','Website'])
        for event in cancellations_additions:
            tsv_writer.writerow(event)
            event.append('Added')
            cancellations_changes.append(event)
        tsv_writer.writerow([now(),'','',''])
    print(now(),"cancellation-additions.tsv saved")
    

if cancellations_removals != []:
    with open('_data/parkrun/cancellation-removals.tsv','wt', encoding='utf-8', newline='') as f:
        tsv_writer = csv.writer(f, delimiter='\t')
        tsv_writer.writerow(['Event','Country','Previous Cancellation Note','Website'])
        for event in cancellations_removals:
            tsv_writer.writerow(event)
            event.append('Removed')
            cancellations_changes.append(event)
        tsv_writer.writerow([now(),'','',''])
    print(now(),"cancellation-removals.tsv saved")

cancellations_changes.sort()

if cancellations_changes != []:
    with open('_data/parkrun/cancellation-changes.tsv','wt', encoding='utf-8', newline='') as f:
        tsv_writer = csv.writer(f, delimiter='\t')
        tsv_writer.writerow(['Event','Country','Cancellation Note','Website','Added or Removed'])
        for event in cancellations_changes:
            tsv_writer.writerow(event)
        tsv_writer.writerow([now(),'','','',''])
    print(now(),"cancellation-changes.tsv saved")

    now_saved = now()
    
    if now_saved.month < 10:
        month = '0'+str(now_saved.month)
    else:
        month = str(now_saved.month)

    if now_saved.day <10:
        day = '0'+str(now_saved.day)
    else:
        day = str(now_saved.day)

    if now_saved.hour < 10:
        hour = '0'+str(now_saved.hour)
    else:
        hour = str(now_saved.hour)

    if now_saved.minute <10:
        minute = '0'+str(now_saved.minute)
    else:
        minute = str(now_saved.minute)

    if now_saved.second <10:
        second = '0'+str(now_saved.second)
    else:
        second = str(now_saved.second)

    file = str(now_saved.year)+'-'+month+'-'+day+'-'+hour+minute+second+'-update.md'

    with open('_posts/Cancellation Updates/'+file, "w+", encoding='utf-8', newline='') as f:
        out = '---' + '\n'
        out += 'layout: post' + '\n'
        out += 'title: '+str(now_saved.year)+'/'+month+'/'+ day +' '+hour+':'+minute+' UTC Update' + '\n'
        out += 'date: '+str(now_saved.year)+'-'+month+'-'+day+' '+hour+':'+minute+':'+second+' +0000' + '\n'
        out += 'author: Cancellations Bot' + '\n'
        out += "category: 'Cancellation Update'" + '\n'
        out += '---' + '\n'
        out += '\n'
        if cancellations_additions != []:
            out += '<h3>New Cancellations</h3>' + '\n'
            out += "<div class='hscrollable'>" + '\n'
            out += "<table style='width: 100%'>" + '\n'
            out += '    <tr>' + '\n'
            out += '        <th>Event</th>' + '\n'
            out += '        <th>Country</th>' + '\n'
            out += '        <th>Cancellation Note</th>' + '\n'
            out += '    </tr>' + '\n'
            for event in cancellations_additions:
                out += '    <tr>' + '\n'
                if event[3] not in ['','Added']:
                    out += '        <td><a href="' + event[3] + '">' + event[0] + '</a></td>' + '\n'
                else:
                    out += '        <td>' + event[0] + '</td>' + '\n'
                out += '        <td>' + event[1] + '</td>' + '\n'
                out += '        <td>' + event[2] + '</td>' + '\n'
                out += '    </tr>' + '\n'
            out += '</table>' + '\n'
            out += '</div>' + '\n'
        if cancellations_removals != []:
            out += '<h3>Cancellations Removed</h3>' + '\n'
            out += "<div class='hscrollable'>" + '\n'
            out += "<table style='width: 100%'>" + '\n'
            out += '    <tr>' + '\n'
            out += '        <th>Event</th>' + '\n'
            out += '        <th>Country</th>' + '\n'
            out += '        <th>Previous Cancellation Note</th>' + '\n'
            out += '    </tr>' + '\n'
            for event in cancellations_removals:
                out += '    <tr>' + '\n'
                if event[3] not in ['','Removed']:
                    out += '        <td><a href="' + event[3] + '">' + event[0] + '</a></td>' + '\n'
                else:
                    out += '        <td>' + event[0] + '</td>' + '\n'
                out += '        <td>' + event[1] + '</td>' + '\n'
                out += '        <td>' + event[2] + '</td>' + '\n'
                out += '    </tr>' + '\n'
            out += '</table>' + '\n'
            out += '</div>' + '\n'
            
        f.write(out)
    print(now(),file,'saved')
    out = 'New Cancellations Update:\nhttps://parkruncancellations.com/'+str(now_saved.year)+'/'+month+'/'+day+'/'+hour+minute+second+'-update/'
    tweet(out)

with open('_data/parkrun/raw/states.tsv','wt', encoding='utf-8', newline='') as f:
    tsv_writer = csv.writer(f, delimiter='\t')
    tsv_writer.writerow(['Event','Country','State','County'])
    for event in new_states_list:
        tsv_writer.writerow(event)
print(now(),'raw/states.tsv saved')

upcoming_events_table.sort()
with open('_data/parkrun/raw/ue.tsv','wt', encoding='utf-8', newline='') as f:
    tsv_writer = csv.writer(f, delimiter='\t')
    tsv_writer.writerow(['Event','Country'])
    for event in upcoming_events_table:
        tsv_writer.writerow([event[0],event[4]])
print(now(),'raw/ue.tsv saved')

def writehistory(file, data):
    try:
        with open('_data/parkrun/history/'+file,'r', encoding='utf-8', newline='\n') as f:
            old_data = json.loads(f.read())
        if now().weekday() == 0 and now().hour <= 1:
            old_data = []
    except FileNotFoundError:
        old_data = []
    print(now(),"history/"+file+" read")
    data['Total']['time'] = str(now())
    old_data.append(countries['Total'])
    with open('_data/parkrun/history/'+file,'wt', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(old_data,indent=4))
    print(now(),"history/"+file+" saved")

writehistory('countries-totals.json',countries)
writehistory('uk-totals.json',uk)
writehistory('aus-totals.json',aus)

print(now(),'Script End')
