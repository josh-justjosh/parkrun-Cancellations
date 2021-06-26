import csv
import datetime

def parse():
    cancellations_changes = []
    with open('_data/parkrun/cancellation-changes.tsv','r', encoding='utf-8', newline='') as f:
        tsv_reader = csv.reader(f, delimiter="\t")
        for row in tsv_reader:
            cancellations_changes.append(row)
            print(row)
    cancellations_changes.remove(['Event','Country','Cancellation Note','Added or<br />Removed'])
    time = cancellations_changes[-1][0]
    cancellations_changes.pop(-1)

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
        writer.writerow(["---"])
        writer.writerow(["layout: post"])
        writer.writerow(['title: '+str(now.year)+"/"+month+"/"+ day +" "+hour+':'+minute+" UTC Update"])
        writer.writerow(['date: '+str(now.year)+"-"+month+"-"+day+" "+hour+':'+minute+':'+second+' 0000'])
        writer.writerow(['author: Josh Brunning'])
        writer.writerow(["---"])
        writer.writerow([])
        writer.writerow(["<table style='width: 100%'>"])
        writer.writerow(["    <tr>"])
        writer.writerow(["        <th>Event</th>"])
        writer.writerow(["        <th>Country</th>"])
        writer.writerow(["        <th>Cancellation Note</th>"])
        writer.writerow(["        <th></th>"])
        writer.writerow(["    </tr>"])
        for event in cancellations_changes:
            writer.writerow(["    <tr>"])
            for cell in event:
                writer.writerow(["        <td>"+cell+"</td>"])
            writer.writerow(["    </tr>"])
    print(file,"saved")
