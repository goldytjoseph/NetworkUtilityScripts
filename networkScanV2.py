#!/usr/bin/python3
import socket
import struct
import sys
import subprocess

# Helper functions to convert between IP addresses and integers

d, s, c = socket.inet_aton, struct, '!I'
f = lambda n: s.pack(c, n)
g = lambda n: socket.inet_ntoa(f(n))

def h(n, b):
    t = 32 - int(b)
    u = s.unpack(c, d(n))[0]
    v = (u >> t) << t
    w = v | ((1 << t) - 1)
    return g(v), g(w), [g(x) for x in range(v, w + 1)]

# Function to ping an IP address
def ping(ip):
    try:
        output = subprocess.check_output(['ping', '-c', '1', '-W', '1', ip])
        if "1 received" in output.decode('utf-8'):
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        return False

<<<<<<< patch-3
def resolve_hostname(ip):
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        return hostname
    except (socket.herror, socket.gaierror):
        return "N/A"

=======
# Check if the correct number of command-line arguments is provided
>>>>>>> main
if len(sys.argv) < 2:
    print("Usage: python subnet_to_iprange.py <subnet>")
    print("Example: python subnet_to_iprange.py 192.168.1.0/24")
    sys.exit(1)

# Parse the subnet argument and calculate the IP range
subnet = sys.argv[1]
start, end, ips = h(*subnet.split('/'))

# Print subnet information
print(f'Subnet: {subnet}')
print(f'IP Range: {start} - {end}')
print('All IPs:')

# Iterate through the list of IPs in the subnet and ping each one
for i in ips:
    status = "up" if ping(i) else "down"
    color = "\033[32m" if status == "up" else "\033[31m"
    hostname = resolve_hostname(i)
    print(f'{color}{i} ({hostname})  \033[0m (Status: {status})')

