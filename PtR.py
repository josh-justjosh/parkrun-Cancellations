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

for i in parkruns:
    print(i)

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
