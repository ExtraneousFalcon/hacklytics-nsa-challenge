import hashlib
import ipaddress
import numpy as np

def calculate_md5_hash(ips, domains):
    ips_sorted = sorted(ips, key=lambda ip: np.uint32(int(ipaddress.ip_address(ip))))
    domains_sorted = sorted(domains)
    hash_input = ", ".join(ips_sorted + domains_sorted)
    return hashlib.md5(hash_input.encode('utf-8')).hexdigest()


ip = ['130.207.161.65', '130.207.248.36', '130.207.184.27', '128.61.61.159', '143.215.224.95']
domain = ['diggydiggyhole.org', 'holein1tunnight.net', 'holistictubes.co.uk', 'mrxq.us', 'shiphulltransports.com']
print(calculate_md5_hash(ip, domain))
