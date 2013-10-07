#!/usr/bin/env python

import socket
import time
import config

def sendData():
    BUFFER = 4096
    sockObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockObj.settimeout(3)
    try:
        sockObj.connect((config.HOST, config.PORT))
        #sockObj.connect(("10.39.80.22", config.PORT))
        sockObj.send(b'IP\n')
        dataRet = sockObj.recv(BUFFER)
        print('Server return:', dataRet.decode())
    except socket.timeout:
        dataRet = b'timeout'
        print(dataRet)
    except socket.error:
        dataRet = b'connection Error'
        print(dataRet)
    sockObj.close()
    return dataRet.decode()

def main():
    while True:
        i = 0
        while i < 5 and sendData() != 'OK\n' :
            time.sleep(1)
            i += 1
        if config.connectType == 'single':
            break
        elif config.connectType == 'continuous':
            time.sleep(60)
            continue
        else:
            print ("config file Error")
            break

if __name__ == '__main__':
    main()
