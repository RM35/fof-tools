from envfof import logpath
from time import sleep
from datetime import datetime


with open(logpath, mode='r', buffering=1) as f:
    while True:
        line = f.readline()
        if line:
            print(line.strip())
        else:
            time.sleep(1)
