import socket
from  threading import Thread
from pynput.mouse import Button, Controller
from screeninfo import get_monitors
from pynput.keyboard import Key, Controller


SERVER = None 
PORT = 8000
IP_ADDRESS = input("Enter your computer IP ADDR : ").strip()
screen_width = None 
screen_height = None

keyboard = Controller()


def recvMessage(client_socket):
    global keyboard
    while True:

        try:
            message = client_socket.recv(2048).decode()

            if(message):
                keyboard.press(message)
                keyboard.release(message)
                print(message)


        except Exception as Error:
            pass    

def getDeviceSize():
    global screen_width
    global screen_height
    for m in get_monitors():
        screen_width = int(str(m).split(",")[2].strip().split('width=')[1])
        screen_height = int(str(m).split(",")[3].strip().split('height=')[1])
        print("screen_height: ",screen_height)
        print("screen_width: ",screen_width)

def acceptConnections():
    global SERVER
    while True:
        client_socket,addr = SERVER.accept()
        print(f"Established connection with {client_socket} with IP {addr}")

        thread  = Thread(target=recvMessage,args=(client_socket,))
        thread.start()

def setup():
    global SERVER
    global  PORT 
    global IP_ADDRESS

    print("\t\t\t\t Welcome to Virtual Keyboard ")
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS,PORT))
    SERVER.listen(10)

    print("\t\t\t SERVER is waiting for incoming connections.\n")

    acceptConnections()
    getDeviceSize()

setup()