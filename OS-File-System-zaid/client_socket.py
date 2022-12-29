import socket

print('** Ready to connect **')
while True:
    host = input('Enter server IP:\t')
    port = 95

    ClientSocket = socket.socket()

    try:
        ClientSocket.connect((host, port))
        print('\t** Connected to server **')
        # print(ClientSocket.getsockname())
        break
    except socket.error as e:
        print("Incorrect IP or server is not running")

while True:
    username = input("Enter username:\t")
    ClientSocket.send(str.encode(username))
    Response = ClientSocket.recv(2048)
    if Response.decode('utf-8') != 'Username is taken':
        break
    print(Response.decode('utf-8'))

print(Response.decode('utf-8'))
while True:
    Input = input('Operation: ')
    if Input == 'BYE':
        ClientSocket.send(str.encode(Input))
        break
    ClientSocket.send(str.encode(Input))
    Response = ClientSocket.recv(2048)
    print(Response.decode('utf-8'))
ClientSocket.close()
