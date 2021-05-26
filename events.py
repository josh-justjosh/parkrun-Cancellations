import json
import csv

with open('_data/raw/events.json') as f:
    events = f.read()

x = json.loads(events)

with open('_data/events.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['id','eventname','EventLongName','EventShortName','LocalisedEventLongName','countrycode','seriesid','EventLocation','Latitude','Longitude'])
    for i in x['events']:
        row = []
        row.append(i['id'])
        row.append(i['properties']['eventname'])
        row.append(i['properties']['EventLongName'])
        row.append(i['properties']['EventShortName'])
        row.append(i['properties']['LocalisedEventLongName'])
        row.append(i['properties']['countrycode'])
        row.append(i['properties']['seriesid'])
        row.append(i['properties']['EventLocation'])
        row.append(i['geometry']['coordinates'][1])
        row.append(i['geometry']['coordinates'][0])
        writer.writerow(row)

with open('_data/events/events.yml', 'w', encoding='utf-8') as f:
    for i in x['events']:
        #f.write('-\n')
        f.write('- id: '+ str(i['id'])+"\n")
        f.write('  eventname: '+ i['properties']['eventname']+"\n")
        f.write('  EventLongName: '+ i['properties']['EventLongName']+"\n")
        f.write('  title: '+ i['properties']['EventShortName']+"\n")
        try:
            f.write('  LocalisedEventLongName: '+ i['properties']['LocalisedEventLongName']+"\n")
        except TypeError:
            pass
        f.write('  countrycode: '+ str(i['properties']['countrycode'])+"\n")
        f.write('  seriesid: '+ str(i['properties']['seriesid'])+"\n")
        f.write('  EventLocation: '+ i['properties']['EventLocation']+"\n")
        f.write('  location:\n')
        f.write('    latitude: '+ str(i['geometry']['coordinates'][1])+"\n")
        f.write('    longitude: '+ str(i['geometry']['coordinates'][0])+"\n\n")
        
