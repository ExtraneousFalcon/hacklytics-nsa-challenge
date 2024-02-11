import pandas as pd
import hashlib
import numpy as np
from datetime import datetime
import ipaddress


def load_dns_logs(filename):

    df = pd.read_csv(
        filename, sep="\t", header=None, names=["timestamp", "ip", "domain"]
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
    return df


cdn_domains = ["cdn.", "akamai.", "cloudfront.", "cdn.cloudflare."]
antivirus_domains = ["update.", "symantec.", "norton.", "avast."]


ignore_patterns = cdn_domains + antivirus_domains


def is_ignored_domain(domain):
    return any(pattern in domain for pattern in ignore_patterns)


def filter_av_cdn_traffic(df):

    df["is_av_cdn"] = df["domain"].apply(is_ignored_domain)

    filtered_df = df[~df["is_av_cdn"]]
    return filtered_df


def detect_dns_tunneling(df):

    df = filter_av_cdn_traffic(df)
    freq_threshold = 10
    df["minute"] = df["timestamp"].dt.floor("T")
    high_freq_ips = df.groupby(["ip", "minute"]).size().reset_index(name="query_count")
    high_freq_ips = high_freq_ips[high_freq_ips["query_count"] > freq_threshold]

    df["top_level_domain"] = df["domain"].apply(lambda x: ".".join(x.split(".")[-2:]))
    df["subdomain"] = df["domain"].apply(lambda x: ".".join(x.split(".")[:-2]))

    length_threshold = 50
    long_domains_df = df[df["subdomain"].str.len() > length_threshold]

    unique_subdomains = (
        df.groupby(["ip", "top_level_domain"])["subdomain"]
        .nunique()
        .reset_index(name="unique_subdomains_count")
    )
    subdomains_threshold = 10
    high_subdomain_ips = unique_subdomains[
        unique_subdomains["unique_subdomains_count"] > subdomains_threshold
    ]

    suspicious_ips = (
        pd.concat(
            [
                high_freq_ips["ip"].drop_duplicates(),
                long_domains_df["ip"].drop_duplicates(),
                high_subdomain_ips["ip"].drop_duplicates(),
            ]
        )
        .drop_duplicates()
        .tolist()
    )

    suspicious_domains = (
        pd.concat(
            [
                long_domains_df["domain"].drop_duplicates(),
                df[df["ip"].isin(suspicious_ips)]["top_level_domain"].drop_duplicates(),
            ]
        )
        .drop_duplicates()
        .tolist()
    )

    return suspicious_ips, suspicious_domains


def calculate_md5_hash(ips, domains):
    ips_sorted = sorted(ips, key=lambda ip: np.uint32(int(ipaddress.ip_address(ip))))
    domains_sorted = sorted(domains)
    hash_input = ", ".join(ips_sorted + domains_sorted)
    return hashlib.md5(hash_input.encode("utf-8")).hexdigest()


def process_dns_logs(filename):
    df = load_dns_logs(filename)
    unique_ips, unique_domains = detect_dns_tunneling(df)
    print(unique_domains)
    result_hash = calculate_md5_hash(unique_ips, unique_domains)
    print(result_hash)


process_dns_logs("dns_logs.txt")
