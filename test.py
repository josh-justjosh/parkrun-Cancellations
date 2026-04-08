"""Local helper: run parkrun_data.py on an interval. Not used in CI."""

import datetime
import subprocess
import sys
import time


def now():
    return datetime.datetime.now().astimezone()


def minsleep(n=1):
    t = ((n - (now().minute % n)) * 60) - (
        now().second + now().microsecond * 0.000001
    )
    print(now(), 'sleeping', str(t) + 's')
    time.sleep(t)


if __name__ == '__main__':
    while True:
        subprocess.run([sys.executable, 'parkrun_data.py'], check=False)
        minsleep(5)
