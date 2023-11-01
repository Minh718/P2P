import socket

# Get the host name
host_name = socket.gethostname()

# Get the IP address associated with the host name
ip_address = socket.gethostbyname(host_name+'.local')

print(f"Host name: {host_name}")
print(f"IP address: {ip_address}")
