import socket
import re

def validate_ip(ip):
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if not re.match(pattern, ip):
        return False
    return all(0 <= int(num) <= 255 for num in ip.split('.'))

def validate_port(port):
    try:
        port = int(port)
        return 1 <= port <= 65535
    except ValueError:
        return False

def validate_mac(mac):
    pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
    return bool(re.match(pattern, mac))

def get_valid_input(prompt, validation_func):
    while True:
        user_input = input(prompt)
        if validation_func(user_input):
            return user_input
        print("Invalid input. Please try again.")

def send_wol_packet(ip_address, port, mac_address):
    mac_bytes = bytes.fromhex(mac_address.replace(':', '').replace('-', ''))
    magic_packet = b'\xff' * 6 + mac_bytes * 16
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    try:
        sock.sendto(magic_packet, (ip_address, port))
        print(f"Wake-on-LAN packet sent to {ip_address}:{port} for MAC {mac_address}")
    except Exception as e:
        print(f"Error sending Wake-on-LAN packet: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    # Get and validate router IP
    router_ip = get_valid_input("Enter the router's IP address: ", validate_ip)

    # Get and validate WoL port
    wol_port = int(get_valid_input("Enter the Wake-on-LAN port (1-65535): ", validate_port))

    # Get and validate device MAC address
    device_mac = get_valid_input("Enter the device's MAC address (format XX:XX:XX:XX:XX:XX or XX-XX-XX-XX-XX-XX): ", validate_mac)

    # Send the Wake-on-LAN packet
    send_wol_packet(router_ip, wol_port, device_mac)
