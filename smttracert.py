#!/usr/bin/python3

from argparse import ArgumentParser
from sys import argv, exit
from xxd import dump
import socket

PORT = 33434


def init_parser():
    parser = ArgumentParser(prog="smttracert.py")
    parser.add_argument("destination", action='store', help="Destination address")
    parser.add_argument("-m", '--max_hops', action='store', dest='hops', default=None, type=type(int),
                        help="Maximum hops number. Default is undefined.")
    return parser


def send_and_get(ttl, dest_address):
    icmp_proto = socket.getprotobyname('icmp')
    udp_proto = socket.getprotobyname('udp')

    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp_proto)
    sender.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

    recv_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp_proto)
    recv_sock.bind(('', PORT))
    recv_sock.settimeout(1)

    sender.sendto(b"My little pony", (dest_address, PORT))
    curr_address = None
    curr_name = None
    try:
        _, curr_address = recv_sock.recvfrom(512)
        dump(_)
        curr_address = curr_address[0]
        try:
            curr_name = socket.gethostbyaddr(curr_address)[0]
        except socket.error:
            curr_name = curr_address
    except socket.timeout:
        pass
    finally:
        sender.close()
        recv_sock.close()
    return curr_address, curr_name


def traceroute(dest, hops):
    dest_address = socket.gethostbyname(dest)
    print(dest_address)
    ttl = 1
    while True:
        answer = send_and_get(ttl, dest_address)
        curr_host = '*'
        if answer[0] is not None:
            curr_host = '{} ({})'.format(*answer)
        yield "Hop {}: {}".format(ttl, curr_host)
        ttl += 1
        if (hops is not None) and (int(hops) < ttl):
            break
        if dest_address == answer[0]:
            break


def main():
    parser = init_parser()
    if len(argv) < 2:
        parser.print_help()
        exit(0)
    args = parser.parse_args(argv[1:])
    for message in traceroute(args.destination, args.hops):
        print(message)


if __name__ == '__main__':
    main()
