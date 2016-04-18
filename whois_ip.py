#!/usr/bin/python3


from sys import argv, exit
import socket
import re
from argparse import ArgumentParser



def whois(dest_addr, whois_server="whois.iana.org", all_msg=False):
    """Returns tuple (netname, asn, country), where netname is network name, asn is Autonomous System Number and country is country (c)your cap"""
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    sock.settimeout(3)
    whois_msg = ""
    try:
        sock.connect((whois_server, 43))
        if whois_server == 'whois.arin.net':
            sock.sendall(b'n ' + dest_addr.encode() + b'\r\n')
        else:
            sock.sendall(dest_addr.encode() + b'\r\n')
        while True:
            buf = sock.recv(1024)
            whois_msg += buf.decode()
            if not buf:
                break
    except socket.timeout:
        print("Server is unreachable.")
    except ConnectionRefusedError:
        print('Server is unreachable.')
    finally:
        sock.close()
    if whois_server == "whois.iana.org":
        p = re.compile(r"refer:\s*(.*)", re.I)
        next_serv = p.findall(whois_msg)
        if not next_serv:
            return None, None, None
        return whois(dest_addr, next_serv[0], all_msg)
    else:
        netname_p = re.compile(r"netname:\s*(.*)", re.I)
        netname = netname_p.findall(whois_msg)
        asn_p = re.compile(r"origin:\s*(.*)", re.I)
        asn = asn_p.findall(whois_msg)
        if not asn:
            ans_p = re.compile(r'originas:\s*(.*)', re.I)
            asn = asn_p.findall(whois_msg)
        country_p = re.compile(r"country:\s*(.*)", re.I)
        country = country_p.findall(whois_msg)
        if all_msg:
            return whois_msg
        return _nof(netname, asn, country)


def _nof(*args):
    """None or first of seq."""
    res = []
    for e in args:
        if not e:
            res.append(None)
            continue
        res.append(e[0])
    return tuple(res)


def addr_to_num(ipv4_addr):
    """Transfer IPv4 address into number."""
    addr = 0
    ipv4_addr = ipv4_addr.split('.')
    for i in range(4):
        addr += int(ipv4_addr[-(i + 1)]) * 256**i
    return addr


def addr_is_white(ipv4_addr):
    """If address is white returns True, else False."""
    addr = addr_to_num(ipv4_addr)
    return not ((addr_to_num("10.0.0.0") <= addr <= addr_to_num("10.255.255.255")) or 
        (addr_to_num("172.16.0.0") <= addr <= addr_to_num("172.31.255.255")) or 
        (addr_to_num("192.168.0.0") <= addr <= addr_to_num("192.168.255.255")) or
        (addr_to_num("127.0.0.1") <= addr <= addr_to_num("127.255.255.255"))
    )


def init_parser():
    parser = ArgumentParser(prog="./whois_ip.py")
    parser.add_argument("IPv4_address", action="store", help="IP address, to which need to check whois.")
    return parser


def main():
    parser = init_parser()
    if not argv[1:]:
        parser.print_help()
    addr = parser.parse_args(argv[1:]).IPv4_address
    print(whois(addr, all_msg=True))


if __name__ == '__main__':
    main()

