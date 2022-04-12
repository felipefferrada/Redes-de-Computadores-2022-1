import socket as s

def mostrar_tablero(gato):
    print(" %c | %c | %c " % (gato[0],gato[1],gato[2]))
    print("---+---+---")
    print(" %c | %c | %c " % (gato[3],gato[4],gato[5]))
    print("---+---+---")
    print(" %c | %c | %c " % (gato[6],gato[7],gato[8]))

def estado_del_juego(gato):
    
    if (gato[0] == gato[1] == gato[2] != ' '):
        estado_actual = "finalizado"
    elif (gato[3] == gato[4] == gato[5] != ' '):
        estado_actual = "finalizado"
    elif (gato[6] == gato[7] == gato[8] != ' '):
        estado_actual = "finalizado"

    elif (gato[0] == gato[3] == gato[6] != ' '):
        estado_actual = "finalizado"
    elif (gato[1] == gato[4] == gato[7] != ' '):
        estado_actual = "finalizado"
    elif (gato[2] == gato[5] == gato[6] != ' '):
        estado_actual = "finalizado"

    elif (gato[0] == gato[4] == gato[8] != ' '):
        estado_actual = "finalizado"
    elif (gato[6] == gato[4] == gato[2] != ' '):
        estado_actual = "finalizado"
    else:
        estado_actual = "jugando"
 
    return estado_actual

addr = 'localhost'
serverPort = 5001
jugadorSocket = s.socket(s.AF_INET, s.SOCK_STREAM)
jugadorSocket.connect((addr, serverPort))

print("-------- Bienvenido al Juego --------")
print("-Seleccione una opcion")
print("1-Jugar\n2-Salir")
opcion = input()

while True:

    if opcion == '2':
        #cerrar el server
        jugadorSocket.send(opcion.encode())
        respuesta = jugadorSocket.recv(1024).decode()
        print("Respuesta del Bot:", respuesta)
        jugadorSocket.close()
        break

    elif opcion == '1':
        jugadorSocket.send(opcion.encode())
        respuesta = jugadorSocket.recv(1024).decode()
        print("Disponibilidad del Bot:", respuesta)
        if respuesta == "NO":
            jugadorSocket.close()
        else:
            gato = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
            jugador_actual = "X" #Human_name
            estado_actual = "jugando"
            turno = 1
            print("Comenzando juego")
            print("El tablero tiene la siguiente estructura\n")
            print(" 1 | 2 | 3 ")
            print("---+---+---")
            print(" 4 | 5 | 6 ")
            print("---+---+---")
            print(" 7 | 8 | 9 \n")
            print("El el jugador X comienza:")

            while(True):
                # se juega

                print("Es el turno del jugador %s" % jugador_actual)

                if jugador_actual == "X":
                    casilla = int(input("Elija una casilla (1-9): \n")) - 1
                else:
                    texto = "Esperando jugada del Bot"  
                    jugadorSocket.send(texto.encode())
                    
                    print(jugadorSocket.recv(1024).decode())
                    casilla = int(jugadorSocket.recv(1024).decode())
                    print("respuesta del Bot: ", casilla)
            
                if casilla >= 0 or casilla <= 8:
            
                    if gato[casilla] != " ":
                        print("La posicion %s ya esta ocupada por favor elija otra" % str(casilla))
                        continue
                    else:
                        gato[casilla] = jugador_actual
                        turno = turno + 1
                else:
                    print("Posicion invalida")
                    continue
            
                mostrar_tablero(gato)
            
                estado_actual = estado_del_juego(gato)
            
                if estado_actual == "jugando":
            
                    if jugador_actual == "X":
                        jugador_actual = "O"
                    else:
                        jugador_actual = "X"
                else:
                    print("El juego ha sido ganado por el jugador %s" % jugador_actual)
                    texto = "FIN"
                    jugadorSocket.send(texto.encode)

                    resp = jugadorSocket.recv(1024).decode()
                    print("respuesta del Bot: ", resp)
                    break
            
                if turno >= 9:
                    print("Ya no existen casillas disponibles esto es un Empate")
                    texto = "FIN"
                    jugadorSocket.send(texto.encode)

                    resp = jugadorSocket.recv(1024).decode()
                    print("respuesta del Bot: ", resp)
                    break

    else:
        opcion = input("opcion invalida")