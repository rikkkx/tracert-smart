#!/usr/bin/python3


from sys import argv, exit
import socket


#  SERVERS = ['whois.arin.net', 'whois.apnic.net', 'whois.ripe.net', 'whois.afrinic.net', 'whois.lacnic.net']
PORT = 43


def whois(dest_addr, whois_server="whois.iana.org"):
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    sock.settimeout(3)

    try:
        sock.connect((whois_server, PORT))
        sock.sendall(dest_addr.encode() + b'\r\n')
        while True:
            buf = sock.recv(1024)
            print(buf.decode())
            if not buf:
                break
    except socket.timeout:
        print("Server is unreachable.")
    except ConnectionRefusedError:
        print('Server is unreachable.')
    finally:
        sock.close()


def main():
    whois(argv[1])


if __name__ == '__main__':
    main()

