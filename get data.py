import datetime
def now():
    return datetime.datetime.utcnow()
print(now(),'Script Start')

import requests
import json

events = requests.get('https://images.parkrun.com/events.json').text.replace("\\u2019","'")

with open('_data/parkrun/raw/events.json','wt', encoding='utf-8', newline='') as f:
    f.write(json.dumps(json.loads(events), indent=2))
    print(now(),"raw/events.json saved")

technical_event_info = requests.get('https://wiki.parkrun.com/index.php/Technical_Event_Information').text

with open('_data/parkrun/raw/tei.html','wt', encoding='utf-8', newline='') as f:
    f.write(technical_event_info)
    print(now(),"raw/tei.html saved")

cancellations = requests.get('https://wiki.parkrun.com/index.php/Cancellations/Global').text.replace("’","'")

with open('_data/parkrun/raw/cancellations.html','wt', encoding='utf-8', newline='') as f:
    f.write(cancellations)
    print(now(),"raw/cancellations.html saved")

print(now(),'Script End')
