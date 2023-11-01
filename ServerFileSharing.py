import socket
import threading
import json
avalFiles = set()
f = open('users.json')
data = json.load(f)
clients = data["users"]

for client in clients:
    for file in client["files"]:
        avalFiles.add(file[1])
f.close()
def handle_client(client_socket, addr):
    message = client_socket.recv(1024).decode()
    print(message)
    if not message:
        for client in clients:
            if addr == client["addrClient"]:
                client['isOnl'] = False
                client['addrClient'] = None
                client['addrServer'] = None
                print(client)
    global avalFiles
    message = json.loads(message)
    command = message["command"]
    data = message["data"]
    if(command=="register"):
        username = data["username"]
        password = data["password"]
        isSuccess = True
        for client in clients:
            if client["username"] == username:
                client_socket.send("fail".encode())
                isSuccess = False
                break
        if isSuccess:
            clients.append({"isOnl": False, "username": username, "password": password, "files": [],"addrClient": addr, "addrServer": None})
            print(clients)
            client_socket.send("success".encode())
    elif(command=="login"):
        username = data["username"]
        password = data["password"]
        for client in clients:
            if client["username"] == username and client["password"] == password:
                client_socket.send("success".encode())
                message = json.loads(client_socket.recv(1024).decode())
                addrServer = tuple(message["addrServer"])
                username = message["username"]
                for client in clients:
                    if username == client["username"]:
                        client["isOnl"] = True
                        client["addrServer"] = addrServer
                        data = json.dumps({
                        "command": "success",
                        "files": client["files"],
                        "avalFiles": list(avalFiles)
                        }).encode()
                        client_socket.send(data)
                        break
                print(clients)
                break
    elif(command=="publishFile"):
        username = data["username"]
        lname = data["lname"]
        fname = data["fname"]
        for client in clients:
            if client["username"] == username:
                client["files"].append((lname, fname))
                avalFiles.add(fname)
                break
    elif(command=="logout"):
        username = data["username"]
        for client in clients:
            if username == client["username"]:
                client['isOnl'] = False
                client['addrServer'] = None
                print(clients)
                break
    elif(command=="fetchFile"):
        fname = data["fname"]
        username= data["username"]
        usersHaveFile = []
        for client in clients:
            if client["username"] != username:
                for file in client["files"]:
                    if file[1] == fname:
                        usersHaveFile.append((client["username"], client["addrServer"], file))
                        break
        data = json.dumps({
                "command": "success",
                "addrUsers": usersHaveFile,
                }).encode()
        client_socket.send(data)
    client_socket.close()
    return

# Server initialization
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('192.168.56.1', 8888))
    server.listen(5)
    print("Server listening on port 8888")

    while True:
        client_socket, addr = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket,addr,))
        client_thread.start()

if __name__ == "__main__":
    main()