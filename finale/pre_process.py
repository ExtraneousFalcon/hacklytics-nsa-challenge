import pandas as pd
import datetime
import socket
import struct

# Function to convert hex timestamp to datetime
def hex_to_datetime(hex_ts):
    return datetime.datetime.utcfromtimestamp(int(hex_ts, 16))

# Function to convert hex IP to string IP
def hex_to_ip(hex_ip):
    return socket.inet_ntoa(struct.pack('!L', int(hex_ip, 16)))

# Function to convert hex to int
def hex_to_int(hex_val):
    return int(hex_val, 16)

# Function to parse a row
def parse_row(row):
    parts = row.split()
    return {
        'ts': hex_to_datetime(parts[0][:-1]),
        'pr': 'tcp',
        'src_ip': hex_to_ip(parts[2].split('.')[0]),
        'src_pt': hex_to_int(parts[2].split('.')[1]),
        'dst_ip': hex_to_ip(parts[3].split('.')[0]),
        'dst_pt': hex_to_int(parts[3].split('.')[1]),
        'cnt': hex_to_int(parts[4]),
        'bts': hex_to_int(parts[5]),
        'flgs': parts[6]
    }

# Read the file
with open('netflows.txt', 'r') as f:
    data = [parse_row(row) for row in f]

# Convert the data to a DataFrame
df = pd.DataFrame(data)
df.to_csv('netflows.csv', index=False)