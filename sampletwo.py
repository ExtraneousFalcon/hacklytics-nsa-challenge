import pandas as pd

df = pd.read_csv('netflows_with_asn.csv')

# Read the list of known attacker IPs
with open('attack.txt', 'r') as f:
    attacker_ips = set(line.strip() for line in f)

# Get the set of unique external IPs in the netflow data
external_ips = set(df['src_ip'])

# Calculate the percentage of external IPs that are listed in the attack file
listed_ips = external_ips & attacker_ips
percentage_listed = len(listed_ips) / len(external_ips) * 100

print(f'{percentage_listed}% of external IPs are listed in the attack file.')

# Check if there are any clients that are listed but also appear to be legitimate clients
# Assuming 'client_ip' is the column in the DataFrame that contains the client IPs
legitimate_clients = set(df['src_ip'])
listed_clients = legitimate_clients & attacker_ips

if listed_clients:
    print('The following clients are listed in the attack file but also appear to be legitimate clients:')
    for ip in listed_clients:
        print(ip)
else:
    print('There are no clients that are listed in the attack file and also appear to be legitimate clients.')