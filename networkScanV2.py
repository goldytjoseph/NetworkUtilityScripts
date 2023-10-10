#!/usr/bin/python3
import socket
import struct
import sys
import subprocess

# Function to convert a subnet into an IP range and check the status of each IP
def subnet_to_ip_range(subnet):
    try:
        d, s, c = socket.inet_aton, struct, '!I'
        f = lambda n: s.pack(c, n)
        g = lambda n: socket.inet_ntoa(f(n))

        def h(n, b):
            t = 32 - int(b)
            u = s.unpack(c, d(n))[0]
            v = (u >> t) << t
            w = v | ((1 << t) - 1)
            return g(v), g(w), [g(x) for x in range(v, w + 1)]

        # Extract start, end, and list of all IPs from the subnet
        start, end, ips = h(*subnet.split('/'))

        print(f'Subnet: {subnet}')
        print(f'IP Range: {start} - {end}')
        print('All IPs:')

        # Check the status (up or down) of each IP address in the range
        for i in ips:
            status = "up" if ping(i) else "down"
            color = "\033[32m" if status == "up" else "\033[31m"
            print(f'{color}{i}  \033[0m')

    except (ValueError, IndexError, socket.error) as e:
        print(f"Error: {e}")
    except subprocess.CalledProcessError:
        print("Error: Unable to execute the 'ping' command.")
    except KeyboardInterrupt:
        print("\nScan interrupted by user.")
        sys.exit(1)

# Function to ping an IP address and check if it's up
def ping(ip):
    try:
        output = subprocess.check_output(['ping', '-c', '1', '-W', '1', ip])
        if "1 received" in output.decode('utf-8'):
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        return False

# Check if the script is being run as the main program
if __name__ == "main":
    if len(sys.argv) < 2:
        print("Usage: python subnet_to_iprange.py <subnet>")
        print("Example: python subnet_to_iprange.py 192.168.1.0/24")
        sys.exit(1)

    subnet = sys.argv[1]
    subnet_to_ip_range(subnet)
