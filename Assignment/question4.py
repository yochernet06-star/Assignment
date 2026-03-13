#!/usr/bin/env python3
import sys
import socket

def get_default_gateway_linux():
    
    try:
        with open('/proc/net/route') as f:
            for line in f.readlines():
                fields = line.strip().split()
                if fields[1] == '00000000' and fields[3] == '0003': 
                    gw_hex = fields[2]
                    gw = socket.inet_ntoa(bytes.fromhex(gw_hex)[::-1])
                    return gw
    except Exception as e:
        print(f"Error reading /proc/net/route: {e}")
    return None

def ip_class(ip):
   
    first_octet = int(ip.split('.')[0])
    if 1 <= first_octet <= 126:
        ip_class = 'A'
        private = (first_octet == 10)
    elif 128 <= first_octet <= 191:
        ip_class = 'B'
        private = (first_octet == 172 and 16 <= int(ip.split('.')[1]) <= 31)
    elif 192 <= first_octet <= 223:
        ip_class = 'C'
        private = (first_octet == 192 and ip.startswith('192.168.'))
    elif 224 <= first_octet <= 239:
        ip_class = 'D (multicast)'
        private = False
    elif 240 <= first_octet <= 255:
        ip_class = 'E (reserved)'
        private = False
    else:
        ip_class = 'Unknown'
        private = False
    return ip_class, private

def main():
    gateway = get_default_gateway_linux()
    if not gateway:
        print("Could not determine default gateway.")
        sys.exit(1)

    print(f"Default Gateway IP: {gateway}")
    cls, private = ip_class(gateway)
    print(f"IP Class: {cls}")
    print(f"Private IP: {'Yes' if private else 'No'}")

if __name__ == "__main__":
    main()
