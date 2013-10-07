#!/usr/bin/env python

import socket
import http.server
import socketserver
import threading

import config

def ipWrite(ipAddr):
    print("Writing IP address to index.html")
    with open('index.html', mode='w', encoding='utf-8') as a_file:
        a_file.write(ipAddr)
    return True

def sockConnect():
    BUFFER = 4096
    sockObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockObj.bind(('0.0.0.0', config.PORT))
    sockObj.listen(1)
    print("Waiting for the client connection at Port:", config.PORT)
    while True:
        connect, (addr,port) = sockObj.accept()
        print("Server is connected by ", addr)
        while True:
            dataRec = connect.recv(BUFFER)
            if dataRec.decode() != 'IP\n':
                break
            else:
                if not ipWrite(addr):
                    print("IP update Error")
                connect.send(b'OK\n')
        connect.close()

def httpServer():
    Handler = http.server.SimpleHTTPRequestHandler
    Handler.path = './'
    httpd = socketserver.TCPServer(("", config.HTTP_PORT), Handler)
    print("HTTP serving at port", config.HTTP_PORT)
    while True:
        httpd.handle_request()

def main():
    threading.Thread(target=sockConnect, args=()).start()
    threading.Thread(target=httpServer, args=()).start()

if __name__ == '__main__':
    main()
