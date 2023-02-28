from envfof import logpath, username, outpath
from time import sleep, time
from datetime import datetime

cleaned_log = []
with open(logpath, mode='r', buffering=1, encoding='utf-8') as f,\
     open(outpath, mode='a', buffering=1, encoding='utf-8') as fo:
    f.seek(0, 2)
    while True:
        line = f.readline()
        if line:
            if line.startswith(f"{username} killed"):
                weapon = line.split("with")[1].rstrip().lstrip()
                vic = line.split("killed")[1].split("with")[0].lstrip().rstrip()
                ts = time()
                s = [ts, "KILLED", vic, weapon]
                print(s)
                fo.write(f"{s[0]},{s[1]},{s[2]},{s[3]}\n")
            if f"killed {username}" in line:
                weapon = line.split("with")[1].rstrip().lstrip()
                killed_by = line.split("killed")[0].rstrip() 
                ts = time()
                s = [ts, "KILLED BY", killed_by, weapon]
                print(s)
                fo.write(f"{s[0]},{s[1]},{s[2]},{s[3]}\n")
        else:
            sleep(1)
