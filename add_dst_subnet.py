import pandas as pd
import ipaddress

# Define the subnets
subnets = [ipaddress.ip_network('128.61.0.0/16'), ipaddress.ip_network('130.207.0.0/16'), 
           ipaddress.ip_network('143.215.0.0/16'), ipaddress.ip_network('192.76.181.0/24')]

# Function to assign each IP to a subnet
def assign_subnet(ip):
    for subnet in subnets:
        if ipaddress.ip_address(ip) in subnet:
            return str(subnet)
    return 'other'

df = pd.read_csv('labeled_netflows.csv')
# Assign each destination IP to a subnet
df['dst_subnet'] = df['dst_ip'].apply(assign_subnet)
df.to_csv('labeled_netflows_with_subnet.csv', index=False)