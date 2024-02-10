import hashlib
import ipaddress


def parse_dns_log(file_path):
    """Parse DNS log file and return a list of tuples with IP addresses and domain names."""
    dns_queries = []
    with open(file_path, "r") as file:
        for line in file:
            _, ip_address, domain_name = line.strip().split("\t")
            dns_queries.append((ip_address, domain_name))
    return dns_queries


def identify_dns_tunneling(dns_queries):
    """Identify potential DNS tunneling based on the length of domain names."""

    suspected_tunnels = [(ip, domain) for ip, domain in dns_queries if len(domain.split(".")[0]) > 20 and "cloudflare" not in domain]
    print(suspected_tunnels[:100])
    return suspected_tunnels


def generate_answer_hash(suspected_tunnels):
    """Generate MD5 hash of sorted IP addresses and domain names."""
    ip_list = [ip for ip, domain in suspected_tunnels]
    dom_list = [domain for ip, domain in suspected_tunnels]

    ip_sorted = [str(x) for x in sorted(ipaddress.ip_address(ip) for ip in ip_list)]
    dom_sorted = sorted(dom_list)

    hash_input = ", ".join(ip_sorted + dom_sorted)
    return hashlib.md5(hash_input.encode("utf-8")).hexdigest()


file_path = "dns_logs.txt"


dns_queries = parse_dns_log(file_path)
suspected_tunnels = identify_dns_tunneling(dns_queries)
answer_hash = generate_answer_hash(suspected_tunnels)

print(answer_hash)
