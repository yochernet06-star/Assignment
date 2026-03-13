#!/usr/bin/env python3
import sys
import socket
import threading
from queue import Queue


THREADS = 100
queue = Queue()
open_ports = []

def scan_port(host, port):
 
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    except socket.error:
        pass

def worker(host):
  
    while not queue.empty():
        port = queue.get()
        scan_port(host, port)
        queue.task_done()

def main():
    if len(sys.argv) != 4:
        print("Usage: python port_scanner.py <target> <start_port> <end_port>")
        sys.exit(1)

    target = sys.argv[1]
    start_port = int(sys.argv[2])
    end_port = int(sys.argv[3])


    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print("Hostname could not be resolved.")
        sys.exit(1)

    print(f"Scanning target: {target_ip} (ports {start_port}-{end_port})")


    for port in range(start_port, end_port + 1):
        queue.put(port)

  
    threads = []
    for _ in range(THREADS):
        t = threading.Thread(target=worker, args=(target_ip,))
        t.start()
        threads.append(t)

  
    queue.join()
    for t in threads:
        t.join()


    if open_ports:
        print("Open ports:")
        for port in sorted(open_ports):
            print(f"  Port {port} is open")
    else:
        print("No open ports found.")

if __name__ == "__main__":
    main()
