#!/usr/bin/python3


from sys import argv, exit
from argparse import ArgumentParser
from socket import error, gethostbyname


def init_argparse():
    parser = ArgumentParser(prog='simple_dns.py')
    parser.add_argument('host', action='store', help="server's domain name.")
    return parser


def main():
    parser = init_argparse()
    if len(argv) < 2:
        parser.print_help()
    host = parser.parse_args(argv[1:]).host
    print(gethostbyname(host))


if __name__ == '__main__':
    try:
        main()
    except error as e:
        print(e)
        exit(0)
