import socket
import json
import threading
import os
import math
import time
serverName = '192.168.56.1'
serverPort = 8888
peerServer = None
hostname = socket.gethostname()
ipLocal = socket.gethostbyname(hostname + '.local')
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
files = []
addrUsers=[]

def sendLogOut():
    global server
    data = json.dumps({
    "command": "logout",
    "data": ""}).encode()
    server.close()
    server = None
    clientSocket.send(data)
    return

def sendRegister(username, password):
    global clientSocket
    data = json.dumps({
    "command": "register",
    "data": {
    "username": username,
    "password": password
    }}).encode()
    clientSocket.send(data)
    message = clientSocket.recv(1024).decode()
    return message

def sendGetUsersFile(fname):
    global clientSocket
    global  addrUsers
    addrUsers = []
    data = json.dumps({
    "command": "fetchFile",
    "data": {
    "fname": fname,
    }}).encode()
    clientSocket.send(data)
    message = json.loads(clientSocket.recv(1024).decode())
    addrUsers = message["addrUsers"]
    users = list(map(lambda user: user[0], addrUsers))
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
            print("oke")
            isSend += 3900
            percent = math.floor((isSend/file_size)*100)
            data = json.dumps({
            "data": l,
            "percent": percent
            }).encode()
            peerClient.send(data)
            l = f.read(3900)
            peerClient.recv(1024).decode()
        f.close()
        peerClient.shutdown(socket.SHUT_WR)
    peerClient.close()
    
def sendLogin(username, password):
    global clientSocket
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
    if message == "success":
        peerServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        peerServer.bind((ipLocal, 0))
        peerServer.listen(1)
        
        threadConn = threading.Thread(target=acceptConnPeer, args=(peerServer,))
        threadConn.start()
        
        data = json.dumps({
        "command": "completeLogin",
        "data": {
        "addrServer": peerServer.getsockname()
        }}).encode()
        clientSocket.send(data)
        message = json.loads(clientSocket.recv(1024).decode())
        files = message["files"]
        avalFiles = message["avalFiles"]
        return (username, files, avalFiles)
    return False
def sendPublishFile(lname, fname):
    global clientSocket
    for file in files:
        if file[0] == lname and file[1] == fname:
            return "File này đã publish"
    data = json.dumps({
    "command": "publishFile",
    "data": {
    "lname": lname,
    "fname": fname
    }}).encode()
    clientSocket.send(data)
    files.append((lname, fname))
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
            time.sleep(0.2)
            clientPeer.send("success".encode())
            mess = clientPeer.recv(4069).decode()
        percent_download.config(text="Đã tải xuống thành công")
        f.close()
        clientPeer.close()
        
def closeApp():
    if peerServer is None: return
    peerServer.close()