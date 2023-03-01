from envfof import logpath, username, outpath
from time import sleep, time
from datetime import datetime
from re import compile

kill = compile(r'^' + username + r'.*killed')
death = compile(r'killed ' + username)
connected = compile(username + r' connected')
end_map = compile(r'END MAP STATS')
close_game = compile(r'^Host_WriteConfiguration')
weapon = compile(r'with (.*)\.')
victim = compile(r'killed (.*) with \w+\.')
killer = compile(r'^(.*) killed')

def parse_kill(line):
    wep = weapon.search(line).group(1)
    vic = victim.search(line).group(1)
    ts = time()
    out = f"{ts:.0f},KILLED,{vic},{wep}"
    print(out)
    return out

def parse_death(line):
    wep = weapon.search(line).group(1)
    killr = killer.search(line).group(1)
    if "+" in killr:
        killr = killr.split("+")[0].rstrip()
    ts = time()
    out = f"{ts:.0f},KILLED_BY,{killr},{wep}"
    print(out)
    return out

def parse_start(line):
    ts = time()
    out = f"{ts:.0f},START"
    print(out)
    return out

def parse_end(line):
    ts = time()
    out = f"{ts:.0f},END"
    print(out)
    return out

with open(logpath, mode='r', buffering=1, encoding='utf-8') as f,\
     open(outpath, mode='a', buffering=1, encoding='utf-8') as fo:
    f.seek(0, 2)
    while True:
        line = f.readline()
        if line:
            if kill.search(line):
                fo.write(parse_kill(line) + "\n")
            if death.search(line):
                fo.write(parse_death(line) + "\n")
            if connected.search(line):
                fo.write(parse_start(line) + "\n")
            if end_map.search(line) or close_game.search(line):
                fo.write(parse_end(line) + "\n")
        else:
            sleep(1)
