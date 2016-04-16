#!/usr/bin/python3


from sys import argv, exit
import socket


SERVER = 'whois.verisign-grs.com'
PORT = 43
ADDR = (SERVER, PORT)


def whois(dest_addr):
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    sock.settimeout(3)
    # dest_addr = socket.gethostbyname(dest_addr)
    try:
        sock.connect(ADDR)
        sock.sendall(dest_addr.encode() + b'\r\n')
        while True:
            buf = sock.recv(1024)
            print(buf.decode())
            if not buf:
                break
    except socket.timeout:
        pass
    except ConnectionRefusedError:
        print('Server is unreachable.')


def main():
    whois(argv[1])


if __name__ == '__main__':
    main()
