import requests
import json
import csv
from bs4 import BeautifulSoup
from html_table_extractor.extractor import Extractor
import datetime
from html.parser import HTMLParser

PtR_Events = []

try:
    ptr_file = str(open('_data/raw/PtR.html', "rb").read())

    class MyHTMLParser(HTMLParser):

        def handle_data(self, data):
            global PtR_Events
            if " parkrun" in data:
                PtR_Events.append(data)

    MyHTMLParser().feed(ptr_file)
    
finally:
    open('_data/raw/PtR.html', "rb").close()

del PtR_Events[:5]
del PtR_Events[-3:]

for i in range(len(PtR_Events)):
    PtR_Events[i] = PtR_Events[i].replace("\\\\n","").replace('\\xe2\\x80\\x99', "'").replace('\\xc3\\xa9', 'e').replace('\\xe2\\x80\\x90', '-').replace('\\xe2\\x80\\x91', '-').replace('\\xe2\\x80\\x92', '-').replace('\\xe2\\x80\\x93', '-').replace('\\xe2\\x80\\x94', '-').replace('\\xe2\\x80\\x94', '-').replace('\\xe2\\x80\\x98', "'").replace('\\xe2\\x80\\x9b', "'").replace('\\xe2\\x80\\x9c', '"').replace('\\xe2\\x80\\x9c', '"').replace('\\xe2\\x80\\x9d', '"').replace('\\xe2\\x80\\x9e', '"').replace('\\xe2\\x80\\x9f', '"').replace('\\xe2\\x80\\xa6', '...').replace('\\xe2\\x80\\xb2', "'").replace('\\xe2\\x80\\xb3', "'").replace('\\xe2\\x80\\xb4', "'").replace('\\xe2\\x80\\xb5', "'").replace('\\xe2\\x80\\xb6', "'").replace('\\xe2\\x80\\xb7', "'").replace('\\xe2\\x81\\xba', "+").replace('\\xe2\\x81\\xbb', "-").replace('\\xe2\\x81\\xbc', "=").replace('\\xe2\\x81\\xbd', "(").replace('\\xe2\\x81\\xbe', ")")

#for i in PtR_Events:
    #print(i)

with open('_data/PtR.tsv','wt', newline='') as f:
    tsv_writer = csv.writer(f, delimiter='\t')
    tsv_writer.writerow(['Event'])
    for i in PtR_Events:
        tsv_writer.writerow([i])
print("PtR.tsv saved")

#with open('_data/PtRtable.csv','w') as f:
#    f.write("Event\n")
#    for i in range(0,len(PtR_Events),2):
#        try:
#            f.write(PtR_Events[i]+", "+PtR_Events[i+1]+"\n")
#        except IndexError:
#            f.write(PtR_Events[i])

def same_week(dateString):
    '''returns true if a dateString in %Y%m%d format is part of the current week'''
    d1 = datetime.datetime.strptime(dateString,'%Y-%m-%d')
    d2 = datetime.datetime.today()
    return d1.isocalendar()[1] == d2.isocalendar()[1] \
              and d1.year == d2.year  

events = requests.get('https://images.parkrun.com/events.json').text.replace("\\u2019","'")
technical_event_info = requests.get('https://wiki.parkrun.com/index.php/Technical_Event_Information').text
cancellations = requests.get('https://wiki.parkrun.com/index.php/Cancellations/Global').text.replace("’","'")

events = json.loads(events)['events']

#with open('_data/raw/technical-event-info.html','w', encoding='utf-8') as f:
#    f.write(technical_event_info)
#print('technical-event-info.html saved')

#with open('_data/raw/cancellations.html','w', encoding='utf-8') as f:
#    f.write(cancellations)
#print('cancellations.html saved')

soup = BeautifulSoup(cancellations, 'html.parser')

extractor = Extractor(soup)
extractor.parse()
cancellation_table = extractor.return_list()
#print(cancellation_table)

cancellations_data = []
cancellations_list = []

for i in range(len(cancellation_table)):
    try:
        for x in range(5):
            cancellation_table[i][x] = cancellation_table[i][x].strip()
    except IndexError:
        break
    if i!=0 and same_week(cancellation_table[i][0]) == True:
        #print(cancellation_table[i])
        cancellations_data.append([cancellation_table[i][1],cancellation_table[i][3],cancellation_table[i][4]])
        cancellations_list.append(cancellation_table[i][1])

cancellation_dates = []


for parkrun in events['features']:
    #print(parkrun['properties']['EventLongName'])
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
        
    if parkrun['properties']['EventLongName'] in PtR_Events:
        parkrun['properties']['Status'] = 'PtR'

    if parkrun['properties']['countrycode'] == 3 :
        parkrun['properties']['Website'] = 'https://www.parkrun.com.au/'+parkrun['properties']['eventname']
        parkrun['properties']['Country'] = 'Australia'
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
        parkrun['properties']['Country'] = 'Sweeden'
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
    
    parkrun['properties']['description']='<h4 style="margin: 0 0 8px;">'+parkrun['properties']['EventLongName']+'</h4><table><tr><th>Status:</th>'
    if parkrun['properties']['Status'] == 'PtR':
        parkrun['properties']['description']+='<td>Permission to Return Received</td>'
    else:
        parkrun['properties']['description']+='<td>'+parkrun['properties']['Status']+'</td>'
    parkrun['properties']['description']+='</tr>'
    
    if parkrun['properties']['ReasonCancelled'] != None:
        parkrun['properties']['description']+='<tr><th>Cancellation Note:</th><td>'+parkrun['properties']['ReasonCancelled']+'</td>'
        parkrun['properties']['description']+='</tr>'
    
    if parkrun['properties']['Website'] != 'Unavailable':
        parkrun['properties']['description']+='<tr><th>Website:</th><td><a href="'+parkrun['properties']['Website']+'">'+parkrun['properties']['Website'].replace('https://www.','')+'</a></td></tr>'
    else: print(parkrun['properties']['EventShortName'],'- Website   Not Generated')    
    parkrun['properties']['description']+='</table>'
    
with open('_data/raw/events.json','w', encoding='utf-8') as f:
    f.write(json.dumps(events))
print('events.json saved')

cancellation_dates = list(dict.fromkeys(cancellation_dates))
with open('_data/cancellation-dates.tsv','wt', encoding='utf-8', newline='') as f:
    tsv_writer = csv.writer(f, delimiter='\t')
    for date in cancellation_dates:
        tsv_writer.writerow([date])
print("cancellation-dates.tsv saved")

cancellations_data.sort()
with open('_data/cancellations.tsv','wt', encoding='utf-8', newline='') as f:
    tsv_writer = csv.writer(f, delimiter='\t')
    tsv_writer.writerow(['Event','Country','Cancellation Note'])
    for event in cancellations_data:
        tsv_writer.writerow(event)
print("cancellations.tsv saved")

events_data  = []
for event in events['features']:
    out = []
    out.append(event['properties']['EventLongName'])
    out.append(event['geometry']['coordinates'][1])
    out.append(event['geometry']['coordinates'][0])
    out.append(event['properties']['Country'])
    out.append(event['properties']['Status'])
    out.append(event['properties']['DateCancelled'])
    out.append(event['properties']['ReasonCancelled'])
    out.append(event['properties']['Website'])
    events_data.append(out)
events_data.sort()

with open('_data/events.tsv','wt', encoding='utf-8', newline='') as f:
    tsv_writer = csv.writer(f, delimiter='\t')
    tsv_writer.writerow(['Event','Latitude','Longitude','Country','Status','DateCancelled','ReasonCancelled','Website'])
    for event in events_data:
        tsv_writer.writerow(event)
print("events.tsv saved")

countries = {
    'Australia': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Permission to Return':0,
        'Total':0
        },
    'Canada': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Permission to Return':0,
        'Total':0
        },
    'Denmark': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Permission to Return':0,
        'Total':0
        },
    'Eswatini': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Permission to Return':0,
        'Total':0
        },
    'Finland': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Permission to Return':0,
        'Total':0
        },
    'France': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Permission to Return':0,
        'Total':0
        },
    'Germany': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Permission to Return':0,
        'Total':0
        },
    'Ireland': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Permission to Return':0,
        'Total':0
        },
    'Italy': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Permission to Return':0,
        'Total':0
        },
    'Japan': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Permission to Return':0,
        'Total':0
        },
    'Malaysia': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Permission to Return':0,
        'Total':0
        },
    'Namibia': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Permission to Return':0,
        'Total':0
        },
    'Netherlands': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Permission to Return':0,
        'Total':0
        },
    'New Zealand': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Permission to Return':0,
        'Total':0
        },
    'Norway': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Permission to Return':0,
        'Total':0
        },
    'Poland': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Permission to Return':0,
        'Total':0
        },
    'Russia': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Permission to Return':0,
        'Total':0
        },
    'Singapore': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Permission to Return':0,
        'Total':0
        },
    'South Africa': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Permission to Return':0,
        'Total':0
        },
    'Sweeden': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Permission to Return':0,
        'Total':0
        },
    'United Kingdom': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Permission to Return':0,
        'Total':0
        },
    'USA': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Permission to Return':0,
        'Total':0
        },
    'Total': {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Permission to Return':0,
        'Total':0
        },
    }

totals= {
        'parkrunning': 0,
        'junior parkrunning':0,
        '5k Cancellations':0,
        'junior Cancellations':0,
        'Permission to Return':0,
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
        countries[parkrun['properties']['Country']]['Permission to Return'] += 1
        countries[parkrun['properties']['Country']]['Total'] += 1
    else:
        print("Error:",parkrun['properties']['EventLongName'])
#print(countries)

for country,data in countries.items():
    totals['parkrunning'] += data['parkrunning']
    totals['junior parkrunning'] += data['junior parkrunning']
    totals['5k Cancellations'] += data['5k Cancellations']
    totals['junior Cancellations'] += data['junior Cancellations']
    totals['Permission to Return'] += data['Permission to Return']
    totals['Total'] += data['Total']

countries['Total'] = totals

with open('_data/countries-data.tsv','wt', encoding='utf-8', newline='') as f:
    tsv_writer = csv.writer(f, delimiter='\t')
    tsv_writer.writerow(['Country','parkrunning','junior parkrunning','5k Cancellations','junior Cancellations','Permission to Return','Total'])
    for i,j in countries.items():
        out = [i]
        for k,l in j.items():
            if l != 0:
                out.append(l)
            else:
                out.append('')
        tsv_writer.writerow(out)
print("countries-data.tsv saved")
