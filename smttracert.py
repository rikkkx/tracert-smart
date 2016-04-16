#!/usr/bin/python3

from argparse import ArgumentParser
from sys import argv, exit
import socket

PORT = 33434


def init_parser():
    parser = ArgumentParser(prog="smttracert.py")
    parser.add_argument("destination", action='store', help="Destination address")
    parser.add_argument("-m", '--max_hops', action='store', dest='hops', default=30, type=type(int),
                        help="Maximum hops number. Default is undefined.")
    return parser


def send_and_get(ttl, dest_address):
    """Creates ICMP package and tries to send it to dest_address.
    Returns IP address of last router and his domain name"""
    icmp = socket.getprotobyname('icmp')

    sender = socket.socket(socket.AF_INET, socket.SOCK_RAW, proto=icmp)
    sender.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

    recv_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, proto=icmp)
    recv_sock.bind(('', PORT))
    recv_sock.settimeout(2)

    p = create_icmp_pack()
    sender.sendto(p, (dest_address, PORT))
    curr_address = None
    curr_name = None
    try:
        curr_address, icmp_msg = parse_icmp(recv_sock.recv(512))
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


def create_icmp_pack():
    #  эхо-запрос пакет с id=42 и sq_num=1
    return b'\x08\x00\xb5\xbc\x42\x42\x00\x01'


def parse_icmp(packet):
    next_proto = packet[9]
    if next_proto != 1:
        raise ValueError("Unknown Protocol")
    dest_addr = ".".join(str_iter(packet[12:16]))
    icmp_type = packet[20]
    icmp_code = packet[21]
    return dest_addr, (icmp_type, icmp_code)


def str_iter(iterable):
    for e in iterable:
        yield str(e)


def traceroute(dest, hops):
    dest_address = socket.gethostbyname(dest)
    yield 'Route to {} [{}] with {} hops max.'.format(dest, dest_address, hops)
    ttl = 1
    while True:
        answer = send_and_get(ttl, dest_address)
        curr_host = '*'
        if answer[0] is not None:
            curr_host = '[{}] {}'.format(*answer)
        yield "{}: {}".format(ttl, curr_host)
        ttl += 1
        if int(hops) < ttl:
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


class TracertException(Exception):
    pass


class UnexpectedProtocolException(TracertException):
    def __init__(self, proto_num):
        self.__msg = "Unexpected protocol: {}".format(proto_num)

    def __str__(self):
        return self.__msg


if __name__ == '__main__':
    try:
        main()
    except PermissionError:
        print("Permission error. Try with sudo.")
        exit(0)
    except KeyboardInterrupt:
        print("\nKeyboard interrupt")
        exit(0)
    except TracertException as e:
        print(e)
        exit(0)

