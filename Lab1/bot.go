package main

import (
	"fmt"
	"math/rand"
	"net"
	"strconv"
	"time"
)

func main() {

	rand.Seed(time.Now().UnixNano())
	dado := rand.Intn(10)

	PORT := ":5000"
	BUFFER := 1024
	s, err := net.ResolveUDPAddr("udp4", PORT)

	if err != nil {
		fmt.Println(err)
		return
	}

	connection, err := net.ListenUDP("udp4", s)
	if err != nil {
		fmt.Println(err)
		return
	}

	defer connection.Close()

	buffer := make([]byte, BUFFER)

	// todos los mensajes del cliente pasan por el servidor intermedio
	fmt.Println("Esperando mensaje del Cliente")
	n, addr, _ := connection.ReadFromUDP(buffer)
	msg := string(buffer[:n])

	if msg == "2" {
		fmt.Println("direccion:", addr)
		fmt.Println("Mensaje del Cliente:", msg)
		response := []byte("ADIOS")
		_, _ = connection.WriteToUDP(response, addr)
		return

	} else {

		if dado == 0 {
			fmt.Println("direccion:", addr)
			fmt.Println("Mensaje del Cliente:", msg)
			response := []byte("NO")
			_, _ = connection.WriteToUDP(response, addr)
			return

		} else {
			fmt.Println("direccion:", addr)
			fmt.Println("Mensaje del Cliente:", msg)
			response := []byte("SI")
			_, _ = connection.WriteToUDP(response, addr)
			for true {
				// se juega
				n, addr, _ := connection.ReadFromUDP(buffer)
				msg := string(buffer[:n])
				fmt.Println("direccion:", addr)
				fmt.Println("Mensaje del Cliente:", msg)
				pos := strconv.Itoa(rand.Intn(8))
				fmt.Println("Respuesta del Bot:", pos)
				response := []byte(pos)
				_, _ = connection.WriteToUDP(response, addr)

				if msg == "FIN" {
					response := []byte("ADIOS")
					_, _ = connection.WriteToUDP(response, addr)
					break
				}

			}
			return
		}

	}

}
