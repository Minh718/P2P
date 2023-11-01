import socket
import json
import threading
import os
import math
import time
serverName = '192.168.56.1'
serverPort = 8888
peerServer = None
name = None
hostname = socket.gethostname()
ipLocal = socket.gethostbyname(hostname + '.local')
files = []
addrUsers=[]

def sendLogOut():
    global peerServer
    global name
    if not peerServer is None:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))
        peerServer.close()
        peerServer = None
        data = json.dumps({
        "command": "logout",
        "data": {"username": name}}).encode()
        clientSocket.send(data)
    return

def sendRegister(username, password):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    data = json.dumps({
    "command": "register",
    "data": {
    "username": username,
    "password": password
    }}).encode()
    clientSocket.send(data)
    message = clientSocket.recv(1024).decode()
    clientSocket.close()
    return message

def sendGetUsersFile(fname):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    global  addrUsers
    addrUsers = []
    data = json.dumps({
    "command": "fetchFile",
    "data": {
    "username": name,
    "fname": fname,
    }}).encode()
    clientSocket.send(data)
    message = json.loads(clientSocket.recv(1024).decode())
    addrUsers = message["addrUsers"]
    users = list(map(lambda user: user[0], addrUsers))
    clientSocket.close()
    return users    

def acceptConnPeer(peerServer):
        while True:
            peerClient, addr = peerServer.accept()
            serverRecvPeer = threading.Thread(target=handle_peer, args=(peerClient,))
            serverRecvPeer.start()
def handle_peer(peerClient):
    message = peerClient.recv(1024).decode()
    message = json.loads(message)
    print(message)
    lname = message["lname"]
    fname = message["fname"]
    file_path = lname + '/' + fname
    print(lname + '/' + fname)
    print(os.path.exists(file_path))
    if os.path.exists(file_path):

        file_size = os.path.getsize(file_path)
        print(file_size)
        isSend = 0
        f = open(file_path, 'r')
    
        l = f.read(3900)
        while l:
            isSend += 3900
            percent = math.floor((isSend/file_size)*100)
            data = json.dumps({
            "data": l,
            "percent": percent
            }).encode()
            peerClient.send(data)
            time.sleep(0.2)
            l = f.read(3900)
        f.close()
        peerClient.shutdown(socket.SHUT_WR)
    peerClient.close()
    
def sendLogin(username, password):
    global name
    name = username
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    global peerServer
    global files
    data = json.dumps({
    "command": "login",
    "data": {
    "username": username,
    "password": password
    }}).encode()
    clientSocket.send(data)
    message = clientSocket.recv(1024).decode()
    if not message:
        return message
    else:
        peerServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        peerServer.bind((ipLocal, 0))
        peerServer.listen(1)
        threadConn = threading.Thread(target=acceptConnPeer, args=(peerServer,))
        threadConn.start()
        print({
        "username": username,
        "addrServer": peerServer.getsockname()
        })
        data = json.dumps({
        "username": username,
        "addrServer": peerServer.getsockname()
        }).encode()
        clientSocket.send(data)
        message = json.loads(clientSocket.recv(1024).decode())
        files = message["files"]
        avalFiles = message["avalFiles"]
        clientSocket.close()
        return (username, files, avalFiles)
def sendPublishFile(lname, fname):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    for file in files:
        if file[0] == lname and file[1] == fname:
            return "File này đã publish"
    data = json.dumps({
    "command": "publishFile",
    "data": {
    "username": name,
    "lname": lname,
    "fname": fname
    }}).encode()
    clientSocket.send(data)
    files.append((lname, fname))
    clientSocket.close()
    return True

def sendFetchFile(user,path_save, percent_download):
    for addrUser in addrUsers:
        print(addrUser, user)
        if addrUser[0] == user:
            print(user)
            threadRecvFile = threading.Thread(target=procRecvFile, args=(addrUser,path_save, percent_download,))
            threadRecvFile.start()
            return
def procRecvFile(addrUser,path_save, percent_download):
        print(addrUser)
        clientPeer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientPeer.connect(tuple(addrUser[1]))
        lname = addrUser[2][0]
        fname = addrUser[2][1]
        data = json.dumps({
        "lname": lname,
        "fname": fname}).encode()
        clientPeer.send(data)
        f = open(path_save+'/'+fname, 'w')
        print(path_save+'/'+fname)
        mess = clientPeer.recv(4069).decode()
        while mess:
            mess = json.loads(mess)
            percent = mess["percent"]
            print(percent)
            data = mess["data"]
            f.write(data)
            percent_download.config(text=f"Đã tải xuống được {percent}%")
            mess = clientPeer.recv(4069).decode()
        percent_download.config(text="Đã tải xuống thành công")
        f.close()
        clientPeer.close()