import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
    print ("Correct usage: script, IP address, port number")
    exit()

IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
#connect to server
server.connect((IP_address, Port))


#change your username
host = socket.gethostname()
host_ip = socket.gethostbyname(host)
while True:
    try:
        if IP_address!=host_ip:
            #receive welcome message from server  
            message = server.recv(2048)
            message = message.decode("utf-8") 
            print(message)
        
        #send user message
        message = bytes(input("<You> "),'utf-8')# fixed error with message not sending because it needed to be in bytes format
        if 'Exit' == message:
            break
        #print(f'Processing Message from input() *****{message}*****')
        server.send(message)
    except Exception as e:
        print("Error in client.py: ",e)
server.close()
            
