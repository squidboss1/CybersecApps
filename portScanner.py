"""

Port Scanner

Usage: python portScanner.py <target_ip> <start_port> <end_port>

"""

import socket
import sys


def scan_ports(target_ip, start_port, end_port):
    try:
        print(f"Starting port scanning on {target_ip}...")
        for port in range(start_port, end_port + 1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target_ip, port))

            if result == 0:
                print(f"Port {port} is open.")
            else:
                print(f"Port {port} is closed. Reason: {socket.errorTab[result]}")

            sock.close()

    except socket.error as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nScanning terminated by the user.")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python scanner.py <target_ip> <start_port> <end_port>")
        sys.exit(1)

    target_ip = sys.argv[1]
    start_port = int(sys.argv[2])
    end_port = int(sys.argv[3])

    if start_port > end_port or start_port <= 0 or end_port > 65535:
        print("Invalid port range.")
        sys.exit(1)

    scan_ports(target_ip, start_port, end_port)
