mport socket
import struct
import sys
import subprocess
import concurrent.futures

# ... (Previous code remains the same)

def scan_ip(ip):
    status = "up" if ping(ip) else "down"
    color = "\033[32m" if status == "up" else "\033[31m"
    print(f'{color}{ip}  \033[0m')

def subnet_to_ip_range(subnet):
    try:
        # ... (Previous code remains the same)

        print(f'Subnet: {subnet}')
        print(f'IP Range: {start} - {end}')
        print('All IPs:')

        # Use ThreadPoolExecutor for parallel scanning
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            # Submit each IP for scanning concurrently
            future_to_ip = {executor.submit(scan_ip, i): i for i in ips}

            # Wait for all tasks to complete
            concurrent.futures.wait(future_to_ip)

    except (ValueError, IndexError, socket.error) as e:
        print(f"Error: {e}")
    except subprocess.CalledProcessError:
        print("Error: Unable to execute the 'ping' command.")
    except KeyboardInterrupt:
        print("\nScan interrupted by user.")
        sys.exit(1)

if name == "main":
    if len(sys.argv) < 2:
        print("Usage: python subnet_to_iprange.py <subnet>")
        print("Example: python subnet_to_iprange.py 192.168.1.0/24")
        sys.exit(1)

    subnet = sys.argv[1]
    subnet_to_ip_range(subnet)
