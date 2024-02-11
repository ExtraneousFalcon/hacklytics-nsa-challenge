import pandas as pd
# Read the list of known attacker IPs
with open('attack.txt', 'r') as f:
    attacker_ips = set(line.strip() for line in f)

# Read the netflow data into a DataFrame
df = pd.read_csv('netflows_with_asn.csv')

# Label the data
df['attacker'] = df['src_ip'].apply(lambda x: x in attacker_ips)

# Convert the boolean labels to integers (optional)
df['attacker'] = df['attacker'].astype(int)

# Save the labeled data
df.to_csv('labeled_netflows.csv', index=False)