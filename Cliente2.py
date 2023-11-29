import socket

def cliente():
#Se crea un objeto de socket para generar la conexion
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #Se Conecta el socket del cliente al servidor en el localhost (127.0.0.1) en el puerto 12345.
    client_socket.connect(('localhost', 12345))
    
#Se recibe del servidor  p, g, y A
    p, g, A = map(int, client_socket.recv(1024).decode().split(','))
    print("Recibido p, g, A desde el servidor.")

    # Leer el mensaje de mensajeentrada.txt
    with open('mensajeentrada.txt', 'r') as archivo_entrada:
        mensaje_original = archivo_entrada.read()

    print("Enviando mensaje al servidor:", mensaje_original)
    
#Se codifica el mensaje en formato bytes y lo envía al servidor.
    client_socket.sendall(mensaje_original.encode())
    
#Se recibe del servidor C1 y C2 .
    C1, *C2 = map(int, client_socket.recv(1024).decode().split(','))
    print("Recibido mensaje cifrado desde el servidor.")

    
#S cierra la conexión del socket del cliente.
    client_socket.close()

if __name__ == "__main__":
    cliente()














