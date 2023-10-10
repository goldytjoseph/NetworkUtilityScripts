import socket
import struct
import sys
import subprocess
import requests

# Constants
PING_TIMEOUT = 1
HTTP_TIMEOUT = 1
PORT_TO_CHECK = 80

# Helper functions
def ip_to_int(ip):
    return struct.unpack('!I', socket.inet_aton(ip))[0]

def int_to_ip(num):
    return socket.inet_ntoa(struct.pack('!I', num))

def subnet_to_range(subnet):
    ip, mask = subnet.split('/')
    mask = int(mask)
    ip_int = ip_to_int(ip)
    subnet_mask = (1 << (32 - mask)) - 1
    start_ip = ip_int & (~subnet_mask)
    end_ip = start_ip | subnet_mask
    return int_to_ip(start_ip), int_to_ip(end_ip)

def is_pingable(ip):
    try:
        subprocess.check_output(['ping', '-c', '1', '-W', str(PING_TIMEOUT), ip])
        return True
    except subprocess.CalledProcessError:
        return False

def is_http_up(ip):
    try:
        response = requests.get(f'http://{ip}', timeout=HTTP_TIMEOUT)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def is_port_open(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((ip, port))
        return True
    except (socket.timeout, ConnectionRefusedError):
        return False

# Main function
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python subnet_to_iprange.py <subnet>")
        print("Example: python subnet_to_iprange.py 192.168.1.0/24")
        sys.exit(1)

    subnet = sys.argv[1]
    start, end = subnet_to_range(subnet)

    print(f'Subnet: {subnet}')
    print(f'IP Range: {start} - {end}')
    print('All IPs:')

    for i in range(ip_to_int(start), ip_to_int(end) + 1):
        ip = int_to_ip(i)
        status = "up" if is_pingable(ip) else "down"
        http_status = "HTTP up" if is_http_up(ip) else "HTTP down"
        port_status = f"Port {PORT_TO_CHECK} up" if is_port_open(ip, PORT_TO_CHECK) else f"Port {PORT_TO_CHECK} down"
        color = "\033[32m" if status == "up" else "\033[31m"
        http_color = "\033[32m" if http_status == "HTTP up" else "\033[31m"
        port_color = "\033[32m" if "up" in port_status else "\033[31m"
        print(f'{color}{ip} (Ping: {status}, HTTP: {http_status}, {port_status})\033[0m')
