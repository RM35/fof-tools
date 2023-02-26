from struct import *
from enum import Enum
from collections import deque

def unp_str(bytes_str):
    """Unpack str from bytes_str and remove any 00 padding"""
    size = len(bytes_str)
    unpacked = unpack(f"<{size}s", bytes_str)[0]
    decoded = unpacked.decode("utf-8")
    stripped = str(decoded).rstrip("\x00")
    return stripped

def unp_int(bytes_int):
    """Unpack int"""
    unpacked = unpack(f"<i", bytes_int)[0] 
    return unpacked

def unp_float(bytes_float):
    """Unpack float"""
    unpacked = unpack(f"<f", bytes_float)[0]
    return unpacked

def unp_uchar(bytes_char):
    """Unpack unsigned char to integer"""
    unpacked = unpack(f"<b", bytes_char)[0] 
    return int(unpacked)

def next_n_bytes(n, filedeque):
    """Retrieve the next n bytes off the file deque, this takes the deque
    via reference so will modify the original as we require it to"""
    b = bytes([bq.popleft() for _ in range(n)])
    return b

class Frametype(Enum):
    """Command types"""
    SIGNON = 1
    PACKET = 2
    SYNCTICK = 3
    CONSOLECMD = 4
    USERCMD = 5
    DATATABLES = 6
    STOP = 7
    STRINGTABLE = 8

with open("big.dem", "rb") as f: demo = f.read()
bq = deque(demo)
total_size = len(bq)

title = unp_str(next_n_bytes(8, bq))
demo_protocol = unp_int(next_n_bytes(4, bq))
network_protocol = unp_int(next_n_bytes(4, bq))
server_name = unp_str(next_n_bytes(260, bq))
client_name = unp_str(next_n_bytes(260, bq))
map_name = unp_str(next_n_bytes(260, bq))
game_dir = unp_str(next_n_bytes(260, bq))
demo_len_sec = unp_float(next_n_bytes(4, bq))
ticks = unp_int(next_n_bytes(4, bq))
frames = unp_int(next_n_bytes(4, bq))
signon_len = unp_int(next_n_bytes(4, bq))

singon = next_n_bytes(signon_len, bq)

output = []

while len(bq) > 0:
    f_type = Frametype(unp_uchar(next_n_bytes(1, bq)))
    print(F"{f_type=}\nAt byte: {total_size - (len(bq)-1)}")
    tick = unp_int(next_n_bytes(4, bq))
    match f_type:
        case Frametype.PACKET:
            next_n_bytes(4, bq)
            x = unp_float(next_n_bytes(4, bq))
            y = unp_float(next_n_bytes(4, bq))
            z = unp_float(next_n_bytes(4, bq))
            next_n_bytes(44, bq)
            size = unp_int(next_n_bytes(4, bq))
            next_n_bytes(size, bq)
            output.append(F"{tick}: {x} {y} {z}")
        case Frametype.SYNCTICK:
            pass
        case Frametype.CONSOLECMD:
            size = unp_int(next_n_bytes(4, bq))
            command = unp_str(next_n_bytes(size, bq))
            output.append(F"CCOMMAND: {command}")
            print(F"{command=}")
        case Frametype.USERCMD:
            next_n_bytes(4, bq)
            size = unp_int(next_n_bytes(4, bq))
            ucommand = unp_str(next_n_bytes(size, bq))
            output.append(F"UCCOMMAND: {ucommand}")
        case Frametype.DATATABLES:
            size = unp_int(next_n_bytes(4, bq))
            next_n_bytes(size, bq)
        case Frametype.STRINGTABLE:
            size = unp_int(next_n_bytes(4, bq))
            next_n_bytes(size, bq)
        case other:
            print("No Match")

with open("out.txt", "w", encoding="utf-8") as f:
    f.writelines(output)

# while len(bq) > 0:
#     frame_type = unp_uchar(next_n_bytes(1, bq))
#     frame_size = unp_int(next_n_bytes(4, bq))
#     frame_data = next_n_bytes(frame_size, bq)
#     print(frame_type)
#     print(frame_size)

print("\n\n\n")
print(F"{title=}")
print(F"{demo_protocol=}")
print(F"{network_protocol=}")
print(F"{server_name=}")
print(F"{client_name=}")
print(F"{map_name=}")
print(F"{game_dir=}")
print(F"{demo_len_sec=}")
print(F"{frames=}")
print(F"{signon_len=}")
