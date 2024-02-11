import pandas as pd
from urllib.parse import urlparse
import tldextract


# Function to check if two strings differ by exactly one letter
def differ_by_one(s1, s2):
    return (len(s1) == len(s2)) and (len(s1) > 15) and (sum(c1 != c2 for c1, c2 in zip(s1, s2)) == 1)

# Load the DNS logs into a DataFrame
df = pd.read_csv('dns_logs.txt', sep='\t', header=None, names=['timestamp', 'ip', 'domain'])

# Extract the base domain from each domain name
df['base_domain'] = df['domain'].apply(lambda x: '.'.join(part for part in [tldextract.extract(x).domain, tldextract.extract(x).suffix] if part))

# Group the DataFrame by base domain
groups = df.groupby('base_domain')

domain = ['diggydiggyhole.org', 'holein1tunnight.net', 'mrxq.us', 'shiphulltransports.com','holistictubes.co.uk']
s = set(df['base_domain'])
for d in domain:
    print(d in s)

# Initialize lists to store the exfiltrating IPs and domains
exfiltrating_ips = []
exfiltrating_domains = []
print(len(groups))
ignore = ['weebly.com', 'webs.com']
# Iterate over each group
for base_domain, group in groups:
    if base_domain in ignore:
        continue
    # Get a list of unique subdomains
    subdomains = group['domain'].apply(lambda x: tldextract.extract(x).subdomain).unique().tolist()
    ips = group['ip'].unique().tolist()
    domains = group['base_domain'].unique().tolist()
    if len(subdomains) < 20:
        continue
    # if len(ips) + len(exfiltrating_ips) > 10:
    #     continue
    cnt = 0
    for i in range(len(subdomains)-1):

        if differ_by_one(subdomains[i], subdomains[i+1]):
            cnt += 1
        if cnt > 20:
            print(subdomains[i], subdomains[i+1])
            exfiltrating_ips.extend(ips)
            exfiltrating_domains.extend(domains)
            break

# Print the exfiltrating IPs and domains
print("Exfiltrating IPs:", exfiltrating_ips)
print("Exfiltrating Domains:", exfiltrating_domains)

