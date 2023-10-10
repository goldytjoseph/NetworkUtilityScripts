#!/usr/bin/python3
import socket
import struct
import sys
import subprocess
import requests

d, s, c = socket.inet_aton, struct, '!I'
f = lambda n: s.pack(c, n)
g = lambda n: socket.inet_ntoa(f(n))

def h(n, b):
    t = 32 - int(b)
    u = s.unpack(c, d(n))[0]
    v = (u >> t) << t
    w = v | ((1 << t) - 1)
    return g(v), g(w), [g(x) for x in range(v, w + 1)]

def ping(ip):
    try:
        output = subprocess.check_output(['ping', '-c', '1', '-W', '1', ip])
        if "1 received" in output.decode('utf-8'):
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        return False

def check_http(ip):
    try:
        response = requests.get(f'http://{ip}', timeout=1)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False

if len(sys.argv) < 2:
    print("Usage: python subnet_to_iprange.py <subnet>")
    print("Example: python subnet_to_iprange.py 192.168.1.0/24")
    sys.exit(1)

subnet = sys.argv[1]
start, end, ips = h(*subnet.split('/'))

print(f'Subnet: {subnet}')
print(f'IP Range: {start} - {end}')
print('All IPs:')

for i in ips:
    status = "up" if ping(i) else "down"
    http_status = "HTTP up" if check_http(i) else "HTTP down"
    color = "\033[32m" if status == "up" else "\033[31m"
    http_color = "\033[32m" if http_status == "HTTP up" else "\033[31m"
    print(f'{color}{i} (Ping: {status}, HTTP: {http_status})\033[0m')
