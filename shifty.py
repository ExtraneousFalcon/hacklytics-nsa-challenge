import pandas as pd
import hashlib
import numpy as np
from datetime import datetime
import ipaddress


# Load the DNS logs from a local file
def load_dns_logs(filename):
    # Assuming the logs are in 'timestamp\tip\tdomain' format
    df = pd.read_csv(filename, sep='\t', header=None, names=['timestamp', 'ip', 'domain'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    return df

cdn_domains = ['cdn.', 'akamai.', 'cloudfront.', 'cdn.cloudflare.']
antivirus_domains = ['update.', 'symantec.', 'norton.', 'avast.']

# Combine lists for a general filter pattern
ignore_patterns = cdn_domains + antivirus_domains

# Filtering function to check if a domain matches any ignore patterns
def is_ignored_domain(domain):
    return any(pattern in domain for pattern in ignore_patterns)



def filter_av_cdn_traffic(df):
    # Apply heuristic check to each domain
    df['is_av_cdn'] = df['domain'].apply(is_ignored_domain)
    # Filter out detected AV/CDN traffic
    filtered_df = df[~df['is_av_cdn']]
    return filtered_df


def detect_dns_tunneling(df):
    # Indicator 1: High frequency of requests
    df = filter_av_cdn_traffic(df)
    freq_threshold = 10  # Example threshold for high frequency
    df['minute'] = df['timestamp'].dt.floor('T')  # Group by minute
    high_freq_ips = df.groupby(['ip', 'minute']).size().reset_index(name='query_count')
    high_freq_ips = high_freq_ips[high_freq_ips['query_count'] > freq_threshold]

    # Indicator 3: High number of unique subdomains
    df['top_level_domain'] = df['domain'].apply(lambda x: '.'.join(x.split('.')[-2:]))
    df['subdomain'] = df['domain'].apply(lambda x: '.'.join(x.split('.')[:-2]))

    # Indicator 2: Long domain names
    length_threshold = 50  # Threshold for long domain names
    long_domains_df = df[df['subdomain'].str.len() > length_threshold]

    unique_subdomains = df.groupby(['ip', 'top_level_domain'])['subdomain'].nunique().reset_index(
        name='unique_subdomains_count')
    subdomains_threshold = 10  # Threshold for a high number of unique subdomains
    high_subdomain_ips = unique_subdomains[unique_subdomains['unique_subdomains_count'] > subdomains_threshold]

    # Combine indicators to identify potential DNS tunneling
    suspicious_ips = pd.concat([
        high_freq_ips['ip'].drop_duplicates(),
        long_domains_df['ip'].drop_duplicates(),
        high_subdomain_ips['ip'].drop_duplicates()
    ]).drop_duplicates().tolist()

    suspicious_domains = pd.concat([
        long_domains_df['domain'].drop_duplicates(),
        df[df['ip'].isin(suspicious_ips)]['top_level_domain'].drop_duplicates()
    ]).drop_duplicates().tolist()

    return suspicious_ips, suspicious_domains


# Calculate the MD5 hash for the lexically sorted concatenation of IPs and domains
def calculate_md5_hash(ips, domains):
    ips_sorted = sorted(ips, key=lambda ip: np.uint32(int(ipaddress.ip_address(ip))))
    domains_sorted = sorted(domains)
    hash_input = ", ".join(ips_sorted + domains_sorted)
    return hashlib.md5(hash_input.encode('utf-8')).hexdigest()


def process_dns_logs(filename):
    df = load_dns_logs(filename)
    unique_ips, unique_domains = detect_dns_tunneling(df)
    print(unique_domains)
    result_hash = calculate_md5_hash(unique_ips, unique_domains)
    print(result_hash)


process_dns_logs('dns_logs.txt')
