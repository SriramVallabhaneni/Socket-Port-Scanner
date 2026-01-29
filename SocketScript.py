# This iteration runs max 100 threads at once
import socket
import threading
import ipaddress

def is_valid_address(ip):
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ValueError:
        return False
    
min_port = 1
max_port = 65535

def is_valid_port_range(range_entered):
    try:
        start, end = map(int, range_entered.split('-'))
        if min_port <= start <= max_port and min_port <= end <= max_port and start <= end:
            return start, end
    except ValueError:
        pass
    return None

while True:
    ip_entered = input("\nEnter the IP address you'd like to scan: ")
    if is_valid_address(ip_entered) == True:
        print(ip_entered + " is valid address")
        break
    print("Invalid ip address, try again")

while True:
    range_entered = input("\nEnter the range of ports you want scanned in the format <int>-<int>?")
    result = is_valid_port_range(range_entered)
    if result:
        start, end = result
        print(range_entered + " is valid range")
        break
    print("Invalid port range, try again")

open_ports = []
lock = threading.Lock()
semaphore = threading.Semaphore(100) # max 100 threads at once

def scan_port(port):
    with semaphore:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            s.connect((ip_entered, port))
            with lock:
                open_ports.append(port)
        except:
            pass
        finally:
            s.close()

threads = []
for port in range (start, end + 1):
    t = threading.Thread(target=scan_port,args=(port,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("\nOpen ports are:", *open_ports)