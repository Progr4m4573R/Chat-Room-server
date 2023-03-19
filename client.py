import socket
import select
import sys

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
    print ("Correct usage: script, IP address, port number")
    exit()

IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
#connect to client
client.connect((IP_address, Port))

#change your username
host = socket.gethostname()
host_ip = socket.gethostbyname(host)

#on connection receive welcome message from server 
message_received = client.recv(2048).decode("utf-8") 
print(message_received)

#take user input
message_sent = bytes(input("<You> "),'utf-8')# fixed error with message not sending because it needed to be in bytes format
while message_sent.lower().strip()!= 'exit':
    try:
        #send user message
        client.send(message_sent)
        
        #receive user messages from server 
        message_received = client.recv(2048).decode("utf-8") 
        print(message_received)
        
        #ask user for input again
        message_sent = bytes(input("<You> "),'utf-8')# fixed error with message not sending because it needed to be in bytes format
    except Exception as e:
        print("Error in client.py: ",e)
client.close()
            
