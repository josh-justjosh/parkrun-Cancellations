import time

def now():
    return datetime.datetime.now().astimezone()

def minsleep(n=1):
    #print(n)
    t = ((n - (now().minute % n)) * 60) - (now().second+now().microsecond*0.000001)
    print(now(), 'sleeping', str(t)+'s')
    time.sleep(t)

while True:
    exec(open("parkrun data.py").read())
    minsleep(5)
