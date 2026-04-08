import datetime


def apply_map_popup_description(properties, now_fn):
    '''Build properties["description"] HTML for map popups (legacy string format).'''
    properties['description'] = '<h4 style="margin: 0 0 8px;">'
    properties['description'] += properties['EventLongName']
    properties['description'] += '</h4><table><tr><th>Status:</th><td'
    if len(properties['Cancellations']) > 1:
        properties['description'] += ' colspan='
        properties['description'] += str(
            len(properties['Cancellations'])) + ' '
    properties['description'] += '>' + \
        properties['Status'] + '</td></tr>'

    if len(properties['Cancellations']) == 1:
        properties['description'] += '<tr><th>Date Cancelled:</th><td>'
        properties['description'] += datetime.datetime.strptime(
            properties['Cancellations'][0]['DateCancelled'],
            '%Y-%m-%d').strftime('%A, %e&nbsp;%B&nbsp;%Y') + '</td></tr>'
        properties['description'] += '<tr><th>Cancellation Note:</th><td>'
        properties['description'] += properties['Cancellations'][0]['ReasonCancelled']
        properties['description'] += '</td></tr>'
    elif len(properties['Cancellations']) > 1:
        properties['description'] += '<tr><th>Date Cancelled:</th>'
        for i in properties['Cancellations']:
            properties['description'] += '<td>' + datetime.datetime.strptime(
                i['DateCancelled'], '%Y-%m-%d').strftime('%A, %e&nbsp;%B&nbsp;%Y') + '</td>'
        properties['description'] += '</tr><tr><th>Cancellation Note:</th>'
        for i in properties['Cancellations']:
            properties['description'] += '<td>' + \
                i['ReasonCancelled'] + '</td>'
        properties['description'] += '</tr>'

    if properties['Website'] != 'Unavailable':
        properties['description'] += '<tr><th>Website:</th><td'
        if len(properties['Cancellations']) > 1:
            properties['description'] += ' colspan=' + \
                str(len(properties['Cancellations'])) + ' '
        properties['description'] += '><a href="' + properties['Website'] + \
            '">' + properties['Website'].replace('https://www.', '') + '</a></td></tr>'
    else:
        print(now_fn(), properties['EventShortName'], '- Website   Not Generated')
    properties['description'] += '</table>'


def apply_special_day_flags(properties, special_events):
    '''Set Thanksgiving / Christmas / Boxing Day / NYD from special_events list.'''
    properties['Special Days'] = {}
    for event in special_events:
        if properties['EventLongName'] == event['EventLongName']:
            try:
                if event["2024-11-28"]:
                    properties["Thanksgiving"] = "parkrunning"
            except KeyError:
                pass
            try:
                if event["2024-12-25"]:
                    properties["Christmas"] = "parkrunning"
            except KeyError:
                pass
            try:
                if event["2024-12-26"]:
                    properties["Boxing Day"] = "parkrunning"
            except KeyError:
                pass
            try:
                if event["2025-01-01"]:
                    properties["NYD"] = "parkrunning"
            except KeyError:
                pass
