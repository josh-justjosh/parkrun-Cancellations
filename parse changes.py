import csv
import datetime

def parse():
    cancellation_changes = []
    with open('_data/cancellation-changes.tsv','r', encoding='utf-8', newline='') as f:
        tsv_reader = csv.reader(f, delimiter="\t")
        for row in tsv_reader:
            cancellation_changes.append(row)
            #print(row)
    cancellation_changes.remove(['Event','Country','Cancellation Note','Added or<br />Removed'])
    time = cancellation_changes[-1][0]
    cancellation_changes.pop(-1)

    cancellations_additions = []
    with open('_data/cancellation-additions.tsv','r', encoding='utf-8', newline='') as f:
        tsv_reader = csv.reader(f, delimiter="\t")
        for row in tsv_reader:
            cancellations_additions.append(row)
            #print(row)
    cancellations_additions.remove(['Event','Country','Cancellation Note'])
    cancellations_additions.pop(-1)

    cancellations_removals = []
    with open('_data/cancellation-removals.tsv','r', encoding='utf-8', newline='') as f:
        tsv_reader = csv.reader(f, delimiter="\t")
        for row in tsv_reader:
            cancellations_removals.append(row)
            #print(row)
    cancellations_removals.remove(['Event','Country','Previous Cancellation Note'])
    cancellations_removals.pop(-1)

    now = datetime.datetime(int(time[0:4]),int(time[5:7]),int(time[8:10]),int(time[11:13]),int(time[14:16]),int(time[17:19]))
    
    if now.month < 10:
        month = '0'+str(now.month)
    else:
        month = str(now.month)

    if now.day <10:
        day = '0'+str(now.day)
    else:
        day = str(now.day)

    if now.hour < 10:
        hour = '0'+str(now.hour)
    else:
        hour = str(now.hour)

    if now.minute <10:
        minute = '0'+str(now.minute)
    else:
        minute = str(now.minute)

    if now.second <10:
        second = '0'+str(now.second)
    else:
        second = str(now.second)

    file = str(now.year)+"-"+month+"-"+day+"-"+hour+minute+second+"-update.md"
    
    with open('_posts/Cancellation Updates/'+file, "w+", encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['---'])
        writer.writerow(['layout: post'])
        writer.writerow(['title: '+str(now.year)+'/'+month+'/'+ day +' '+hour+':'+minute+' UTC Update'])
        writer.writerow(['date: '+str(now.year)+'-'+month+'-'+day+' '+hour+':'+minute+':'+second+' +0000'])
        writer.writerow(['author: Cancellations Bot'])
        writer.writerow(['---'])
        writer.writerow([])
        if cancellations_additions != []:
            writer.writerow(['<h3>New Cancellations</h3>'])
            writer.writerow(["<table style='width: 100%'>"])
            writer.writerow(['    <tr>'])
            writer.writerow(['        <th>Event</th>'])
            writer.writerow(['        <th>Country</th>'])
            writer.writerow(['        <th>Cancellation Note</th>'])
            writer.writerow(['    </tr>'])
            for event in cancellations_additions:
                writer.writerow(['    <tr>'])
                for cell in event:
                    towrite = '        <td>'+cell+'</td>'
                    writer.writerow([towrite.replace('"','')])
                writer.writerow(['    </tr>'])
            writer.writerow(['</table>'])
        if cancellations_removals != []:
            writer.writerow(['<h3>Cancellations Removed</h3>'])
            writer.writerow(["<table style='width: 100%'>"])
            writer.writerow(['    <tr>'])
            writer.writerow(['        <th>Event</th>'])
            writer.writerow(['        <th>Country</th>'])
            writer.writerow(['        <th>Previous Cancellation Note</th>'])
            writer.writerow(['    </tr>'])
            for event in cancellations_removals:
                writer.writerow(['    <tr>'])
                for cell in event:
                    towrite = '        <td>'+cell+'</td>'
                    writer.writerow([towrite.replace('"','')])
                writer.writerow(['    </tr>'])
            writer.writerow(['</table>'])
    print(file,'saved')
