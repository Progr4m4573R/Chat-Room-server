import socket
from _thread import *
import sys
#We made a socket object and reserved a port on our pc.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
"""
the first argument AF_INET is the address domain of the socket. This is used when we have an Internet Domain
with any two hosts
The second argument is the type of socket. SOCK_STREAM means that data or characters are read in a continuous flow
"""
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.bind((IP_address, Port)) 
#binds the server to an entered IP address and at the specified port number. The client must be aware of these parameters
server.listen(100)
#listens for 100 active connections. This number can be increased as per convenience
list_of_clients=[]
list_of_addr=[]

def clientthread(conn, addr):
    #Convert string to bytes so it can be sent source: https://stackoverflow.com/questions/7585435/best-way-to-convert-string-to-bytes-in-python-3
    #sends a message to the client whose user object is conn
    conn.send(bytes(('Welcome to the chatroom!'),'utf-8'))
    while True:
        try:
            #Recieve message from client and decode bytes to string for concatination
            message = conn.recv(2048).decode("utf-8")  
            if not(message):
                break
            #fixed Error with clientthread function not being able to concatinate bytes  source: https://stackoverflow.com/questions/606191/convert-bytes-to-a-string
            #prints the message and address of the user who just sent the message on the server terminal
            print("<" + addr[0] + "> says: " + message)
            message_to_send = "<" + addr[0] + "> says: " + message
            broadcast(message_to_send,conn,addr)

        except Exception as e:
            print ("Error occured in clientthread: ", e)
            remove(conn,addr)
            
def broadcast(message,conn,addr):
    #You cannot send a message from the same ip as the server or this code will not run
    #hostname=socket.gethostname()
    #server_addr = socket.gethostbyname(hostname)
    # print("device ip: ",addr)
    # print("server ip: ",server_addr)
    #If the ip address of device sending message is different to the server device then run

    try:
        #Allows server to send messages
        # server_message = input('<Server>: ')
        # message_to_send = "<Server>:*** " +server_message+" ***"
        # conn.send(message_to_send.encode())
        conn.send(message.encode())
    except Exception as e:
        print("Error occured in broadcast: ",e)
        conn.close()
        remove(conn,addr)

def remove(connection,addr):
    try:
        if connection in list_of_clients:
            list_of_clients.remove(connection)
            print(addr[0],"left the chat.")
    except Exception as e:
        print("Error occured in remove: ",e)
        
while True:
    try:
        conn, addr = server.accept()
        """
        Accepts a connection request and stores two parameters, conn which is a socket object for that user, and addr which contains
        the IP address of the client that just connected
        """
        list_of_clients.append(conn)
        list_of_addr.append(addr)
        print(addr[0] + " joined the chat.")
        #maintains a list of clients for ease of broadcasting a message to all available people in the chatroom
        #Prints the address of the person who just connected
        start_new_thread(clientthread,(conn,addr))
        
        #creates and individual thread for every user that connects
    except Exception as e:
        print("Error occured in chat_server.py, main: ",e)
        break
conn.close()
