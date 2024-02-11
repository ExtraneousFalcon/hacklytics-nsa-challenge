import pandas as pd
import ipaddress
from tqdm import tqdm

# Function to convert IP to integer
def ip_to_int(ip):
    return int(ipaddress.IPv4Address(ip))

# Function to get the ASN for an IP address
def get_asn(ip, asn_df):
    ip_int = ip_to_int(ip)
    mask = (asn_df['start_ip'] <= ip_int) & (asn_df['end_ip'] >= ip_int)
    asn_info = asn_df[mask]
    if not asn_info.empty:
        return asn_info.iloc[0]['asn']
    else:
        return None

# Read the ASN data into a DataFrame
asn_df = pd.read_csv('asn.csv')

# Filter out IPv6 ranges
asn_df = asn_df[asn_df['start_ip'].apply(lambda x: ':' not in x)]

asn_df['start_ip'] = asn_df['start_ip'].apply(ip_to_int)
asn_df['end_ip'] = asn_df['end_ip'].apply(ip_to_int)

# Read the netflow data into a DataFrame
df = pd.read_csv('netflows.csv')

# Get the ASN for each source IP address with tqdm progress bar
df['src_asn'] = [get_asn(x, asn_df) for x in tqdm(df['src_ip'])]
df.to_csv('netflows_with_asn.csv', index=False)

# Calculate the statistics
most_common_asn = df['src_asn'].value_counts().idxmax()
most_distinct_ips_asn = df.groupby('src_asn')['src_ip'].nunique().idxmax()

print(f'The ASN that connects the most often is: {most_common_asn}')
print(f'The ASN that has the most distinct IP addresses is: {most_distinct_ips_asn}')