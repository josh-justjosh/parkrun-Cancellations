import requests
import json

events = requests.get('https://images.parkrun.com/events.json')
technical_event_info = requests.get('https://wiki.parkrun.com/index.php/Technical_Event_Information')
cancellations = requests.get('https://wiki.parkrun.com/index.php/Cancellations/Global')

features = json.loads(events.text)['events']['features']
events = {'events':features}

with open('_data/raw/events.json','w', encoding='utf-8') as f:
    f.write(json.dumps(events))
print('events.json saved')

with open('_data/raw/technical-event-info.html','w', encoding='utf-8') as f:
    f.write(technical_event_info.text)
print('technical-event-info.html saved')

with open('_data/raw/cancellations.html','w', encoding='utf-8') as f:
    f.write(cancellations.text)
print('cancellations.html saved')
