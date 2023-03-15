import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
    print ("Correct usage: script, IP address, port number")
    exit()

IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.connect((IP_address, Port))

#welcome message  
message = server.recv(2048)
print(message)

while True:
    try:#user message
        message = bytes(input("<You> "),'utf-8')# fixed error with message not sending because it needed to be in bytes format
        if 'Exit' == message:
            break
        #print(f'Processing Message from input() *****{message}*****')
        server.send(message)
    except Exception as e:
        print("Error in client.py: ",e)
server.close()
            