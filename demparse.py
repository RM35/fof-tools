from struct import *
import traceback

def dem_str(size: int, fileobj):
    unpacked = unpack(f"<{size}s", fileobj.read(size))[0]
    decoded = unpacked.decode("utf-8")
    stripped = str(decoded).rstrip("\x00")
    return stripped

def dem_int(fileobj):
    unpacked = unpack(f"<i", fileobj.read(4))[0]
    return unpacked

def dem_float(fileobj):
    unpacked = unpack(f"<f", fileobj.read(4))[0]
    return unpacked

with open("test.dem", "rb") as f:
    title = dem_str(8, f)
    demo_protocol = dem_int(f)
    network_protocol = dem_int(f)
    server_name = dem_str(260, f) 
    client_name = dem_str(260, f)
    map_name = dem_str(260, f)
    game_dir = dem_str(260, f)
    demo_len_sec = dem_float(f)
    ticks = dem_int(f)
    frames = dem_int(f)
    signon_len = dem_int(f)

print(F"{title=}")
print(F"{demo_protocol=}")
