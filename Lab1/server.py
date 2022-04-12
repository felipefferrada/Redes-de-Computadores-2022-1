import socket as s

addr = 'localhost'

botPuerto = 5000
botSocket = s.socket(s.AF_INET, s.SOCK_DGRAM)

clientePuerto = 5001
clienteSocket = s.socket(s.SOCK_DGRAM)
clienteSocket.bind(('', clientePuerto))
clienteSocket.listen(1)

jugadorSocket, jugadorAddr = clienteSocket.accept()
msg = jugadorSocket.recv(1024).decode()
print("Mensaje del Cliente:", msg)

botSocket.sendto(msg.encode(), (addr, botPuerto))
msg, addr = botSocket.recvfrom(1024)
print("Mensaje del Bot:", msg.decode())
jugadorSocket.send(msg)



if msg.decode() == "SI":
    # se juega
    while True:
        msg = jugadorSocket.recv(1024).decode()
        print("Mensaje del Cliente:", msg)
        botSocket.sendto(msg.encode(), addr)

        msg, addr = botSocket.recvfrom(1024)
        print("Mensaje del Bot:", msg.decode())
        jugadorSocket.send(msg)

        if msg == "ADIOS":
            break
