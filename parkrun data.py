import requests
import json
import csv
from bs4 import BeautifulSoup
from html_table_extractor.extractor import Extractor
import datetime
from html.parser import HTMLParser

parkruns = []

try:
    ptr_file = str(open('_data/raw/PtR.html', "rb").read())

    class MyHTMLParser(HTMLParser):

        def handle_data(self, data):
            global parkruns
            if " parkrun" in data:
                parkruns.append(data)

    MyHTMLParser().feed(ptr_file)
    
finally:
    open('_data/raw/PtR.html', "rb").close()

del parkruns[:5]
del parkruns[-4:]

for i in range(len(parkruns)):
    parkruns[i] = parkruns[i].replace("\\\\n","").replace('\\xe2\\x80\\x99', "'").replace('\\xc3\\xa9', 'e').replace('\\xe2\\x80\\x90', '-').replace('\\xe2\\x80\\x91', '-').replace('\\xe2\\x80\\x92', '-').replace('\\xe2\\x80\\x93', '-').replace('\\xe2\\x80\\x94', '-').replace('\\xe2\\x80\\x94', '-').replace('\\xe2\\x80\\x98', "'").replace('\\xe2\\x80\\x9b', "'").replace('\\xe2\\x80\\x9c', '"').replace('\\xe2\\x80\\x9c', '"').replace('\\xe2\\x80\\x9d', '"').replace('\\xe2\\x80\\x9e', '"').replace('\\xe2\\x80\\x9f', '"').replace('\\xe2\\x80\\xa6', '...').replace('\\xe2\\x80\\xb2', "'").replace('\\xe2\\x80\\xb3', "'").replace('\\xe2\\x80\\xb4', "'").replace('\\xe2\\x80\\xb5', "'").replace('\\xe2\\x80\\xb6', "'").replace('\\xe2\\x80\\xb7', "'").replace('\\xe2\\x81\\xba', "+").replace('\\xe2\\x81\\xbb', "-").replace('\\xe2\\x81\\xbc', "=").replace('\\xe2\\x81\\xbd', "(").replace('\\xe2\\x81\\xbe', ")")

#for i in parkruns:
    #print(i)

with open('_data/PtR.csv','w') as f:
    f.write("Event\n")
    for i in parkruns:
        f.write(i+"\n")

with open('_data/PtRtable.csv','w') as f:
    f.write("Event\n")
    for i in range(0,len(parkruns),2):
        try:
            f.write(parkruns[i]+", "+parkruns[i+1]+"\n")
        except IndexError:
            f.write(parkruns[i])

def same_week(dateString):
    '''returns true if a dateString in %Y%m%d format is part of the current week'''
    d1 = datetime.datetime.strptime(dateString,'%Y-%m-%d')
    d2 = datetime.datetime.today()
    return d1.isocalendar()[1] == d2.isocalendar()[1] \
              and d1.year == d2.year  

events = requests.get('https://images.parkrun.com/events.json').text
technical_event_info = requests.get('https://wiki.parkrun.com/index.php/Technical_Event_Information').text
cancellations = requests.get('https://wiki.parkrun.com/index.php/Cancellations/Global').text

events = json.loads(events)['events']

#with open('_data/raw/technical-event-info.html','w', encoding='utf-8') as f:
#    f.write(technical_event_info)
#print('technical-event-info.html saved')

#with open('_data/raw/cancellations.html','w', encoding='utf-8') as f:
#    f.write(cancellations)
#print('cancellations.html saved')

PtR = []
with open('_data/PtR.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        for cell in row:
            PtR.append(cell)
PtR.remove("Event")

soup = BeautifulSoup(cancellations, 'html.parser')

extractor = Extractor(soup)
extractor.parse()
cancellation_table = extractor.return_list()
#print(cancellation_table)

cancellations_list = []

for i in range(len(cancellation_table)):
    try:
        for x in range(5):
            cancellation_table[i][x] = cancellation_table[i][x].strip()
    except IndexError:
        break
    if i!=0 and same_week(cancellation_table[i][0]) == True:
        #print(cancellation_table[i])
        cancellations_list.append(cancellation_table[i][1])

cancellation_dates = []

for parkrun in events['features']:
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
        
    if parkrun['properties']['EventLongName'] in PtR:
        parkrun['properties']['Status'] = 'PtR'

    if parkrun['properties']['countrycode'] == 3 : parkrun['properties']['Website'] = 'https://www.parkrun.com.au/'+parkrun['properties']['eventname']
    elif parkrun['properties']['countrycode'] == 14 : parkrun['properties']['Website'] = 'https://www.parkrun.ca/'+parkrun['properties']['eventname']
    elif parkrun['properties']['countrycode'] == 23 : parkrun['properties']['Website'] = 'https://www.parkrun.dk/'+parkrun['properties']['eventname']
    elif parkrun['properties']['countrycode'] == 30 : parkrun['properties']['Website'] = 'https://www.parkrun.fi/'+parkrun['properties']['eventname']
    elif parkrun['properties']['countrycode'] == 31 : parkrun['properties']['Website'] = 'https://www.parkrun.fr/'+parkrun['properties']['eventname']
    elif parkrun['properties']['countrycode'] == 32 : parkrun['properties']['Website'] = 'https://www.parkrun.com.de/'+parkrun['properties']['eventname']
    elif parkrun['properties']['countrycode'] == 42 : parkrun['properties']['Website'] = 'https://www.parkrun.ie/'+parkrun['properties']['eventname']
    elif parkrun['properties']['countrycode'] == 44 : parkrun['properties']['Website'] = 'https://www.parkrun.it/'+parkrun['properties']['eventname']
    elif parkrun['properties']['countrycode'] == 46 : parkrun['properties']['Website'] = 'https://www.parkrun.jp/'+parkrun['properties']['eventname']
    elif parkrun['properties']['countrycode'] == 57 : parkrun['properties']['Website'] = 'https://www.parkrun.my/'+parkrun['properties']['eventname']
    elif parkrun['properties']['countrycode'] == 65 : parkrun['properties']['Website'] = 'https://www.parkrun.co.nz/'+parkrun['properties']['eventname']
    elif parkrun['properties']['countrycode'] == 67 : parkrun['properties']['Website'] = 'https://www.parkrun.no/'+parkrun['properties']['eventname']
    elif parkrun['properties']['countrycode'] == 74 : parkrun['properties']['Website'] = 'https://www.parkrun.pl/'+parkrun['properties']['eventname']
    elif parkrun['properties']['countrycode'] == 79 : parkrun['properties']['Website'] = 'https://www.parkrun.ru/'+parkrun['properties']['eventname']
    elif parkrun['properties']['countrycode'] == 82 : parkrun['properties']['Website'] = 'https://www.parkrun.sg/'+parkrun['properties']['eventname']
    elif parkrun['properties']['countrycode'] == 85 : parkrun['properties']['Website'] = 'https://www.parkrun.co.za/'+parkrun['properties']['eventname']
    elif parkrun['properties']['countrycode'] == 88 : parkrun['properties']['Website'] = 'https://www.parkrun.se/'+parkrun['properties']['eventname']
    elif parkrun['properties']['countrycode'] == 97 : parkrun['properties']['Website'] = 'https://www.parkrun.org.uk/'+parkrun['properties']['eventname']
    elif parkrun['properties']['countrycode'] == 98 : parkrun['properties']['Website'] = 'https://www.parkrun.us/'+parkrun['properties']['eventname']
    elif parkrun['properties']['countrycode'] == 64 : parkrun['properties']['Website'] = 'https://www.parkrun.co.nl/'+parkrun['properties']['eventname']
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
    else: print(parkrun['properties']['EventShortName'],'- Website Not Generated')    
    parkrun['properties']['description']+='</table>'
    
with open('_data/raw/events.json','w', encoding='utf-8') as f:
    f.write(json.dumps(events))
print('events.json saved')

cancellation_dates = list(dict.fromkeys(cancellation_dates))
with open('_data/cancellation-dates.csv','w', encoding='utf-8') as f:
    for date in cancellation_dates:
        f.write(date+"\n")
print("cancellation-dates.csv saved")
