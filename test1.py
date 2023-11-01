import socket

import time
# Tạo socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))
server_socket.listen(5)

# Biến cờ để kiểm tra khi nào đóng
server_closed = False

try:
    while not server_closed:
        print("Waiting for a connection...")
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        # Thực hiện xử lý kết nối ở đây

except KeyboardInterrupt:
    # Bắt sự kiện Ctrl+C để đóng server
    server_closed = True
    print("Closing the server...")

# Đóng socket server và tất cả các kết nối đã tồn tại
server_socket.close()
