
#This program module consists of the functions required to interface the sesnsors to the edge computer

import socket               #for implementing socketprogramming for the UDP Server
import serial               #for implementing the the serial port for receving data from the bluetooth modules

#defining the IP,Port and buffersize for the UDP Server
localIP     = "127.0.0.1"       
localPort   = 2017
bufferSize  = 1024
msgFromServer1       = "Send climate data"
bytesToSend1         = str.encode(msgFromServer1) #convert the string to bytes format
msgFromServer2       = "Data received"
bytesToSend2         = str.encode(msgFromServer2)
# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

def udpdatasensor03():
    # Bind to address and ip
    UDPServerSocket.bind((localIP, localPort))
    print("UDP server up and listening")

    UDPServerSocket.sendto(bytesToSend1, address)               #sends the first message to the UDP client

    # Listen for incoming datagrams
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)     #received the data from the UDP Client      
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    clientIP  = "Client IP Address:{}".format(address)          #print the client IP address
    print(clientIP)
    # Sending a reply to client
    UDPServerSocket.sendto(bytesToSend2, address)              #send the second message to the UDP Client
    data =message.decode('utf-8')                              #converting the bytes received from UDP client to string
    return data

def serialdatasensor04():
    ser = serial.Serial(                                       #declaring serial connection
        port = 'COM2',
        baudrate = 115200,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 10
        )
    print("Connection established...")
    ser.write(b'\x02')                                      #sending 02 command that tells the serial port to send sensor data
    data = ser.readline().decode()                          #reading the data received and converting bytes format to string format
    return data

def serialdatasensor05():
    ser = serial.Serial(                                    #declaring serial connection
        port = 'COM4',
        baudrate = 115200,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 10
        )
    print("Connection established...")
    ser.write(b'\x02')                                      #sending 02 command that tells the serial port to send sensor data
    data = ser.readline().decode()                          #reading the data received and converting  bytes format to string format
    return data