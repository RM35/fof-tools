from envfof import logpath, username, outpath
from time import sleep, time
from datetime import datetime
from re import compile

kill = compile(username + r'.*killed')
death = compile(r'killed ' + username)
connected = compile(username + r' connected')
end_map = compile(r'END MAP STATS')
weapon = compile(r'with (\w+)\.')
victim = compile(

def parse_kill(line):
    weapon = line.split("with")[1].rstrip().lstrip()
    vic = line.split("killed")[1].split("with")[0].lstrip().rstrip()
    ts = time()
    s = [ts, "KILLED", vic, weapon]
    print(s)
    fo.write(f"{s[0]},{s[1]},{s[2]},{s[3]}\n")

def parse_death(line):
    weapon = line.split("with")[1].rstrip().lstrip()
    killed_by = line.split("killed")[0].rstrip() 
    ts = time()
    s = [ts, "KILLED BY", killed_by, weapon]
    print(s)
    fo.write(f"{s[0]},{s[1]},{s[2]},{s[3]}\n")

with open(logpath, mode='r', buffering=1, encoding='utf-8') as f,\
     open(outpath, mode='a', buffering=1, encoding='utf-8') as fo:
    f.seek(0, 2)
    while True:
        line = f.readline()
        if line:
            if kill.search(line):
                parse_kill(line)
            if death.search(line):
                parse_death(line)
            if connected.search(line):
                pass
            if end_map.search(line):
                pass
        else:
            sleep(1)
