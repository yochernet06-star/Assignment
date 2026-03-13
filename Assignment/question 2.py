#!/usr/bin/env python3
import sys
import nmap

def main():
    if len(sys.argv) < 2:
        print("Usage: python nmap_scanner.py <target> [ports]")
        print("  ports format: e.g., '22', '1-1000', '22,80,443'")
        sys.exit(1)

    target = sys.argv[1]
    ports = sys.argv[2] if len(sys.argv) > 2 else '1-1024'  

 
    nm = nmap.PortScanner()

    print(f"Scanning {target} for ports {ports}...")

    
    try:
        nm.scan(hosts=target, ports=ports, arguments='-sS')
    except Exception as e:
        print(f"Scan failed: {e}")
        sys.exit(1)


    for host in nm.all_hosts():
        print(f"\nHost: {host} ({nm[host].hostname()})")
        print(f"State: {nm[host].state()}")
        for proto in nm[host].all_protocols():
            print(f"Protocol: {proto}")
            ports = nm[host][proto].keys()
            for port in sorted(ports):
                state = nm[host][proto][port]['state']
                print(f"  Port {port}: {state}")

if __name__ == "__main__":
    main()
