import socket
import random

def generar_claves():
    # Definimos parámetros públicos p y g 
    p = 23
    g = 5
    
    #a es un numero aleatorio a en el rango [1, p-1]
    a = random.randint(1, p-1)
    
    # A calcula la llave publica usando la clave privada a, p y g
    A = pow(g, a, p)
    
    #Se retornan los parámetros p, g, la clave privada a y la clave pública A
    return p, g, a, A

def cifrar(mensaje, p, g, A):
    # Generar un número aleatorio k en el rango [1, p-1]
    k = random.randint(1, p-1)
    
    # K es la llave privada, se calcula usando A y k
    K = pow(A, k, p)
    
    # C1 es primera componente del mensaje cifrado
    C1 = pow(g, k, p)
    
    #Se calcula la componente cifrada C2  y se consideran letras de la A a la Z
    C2 = [(ord(char) - ord('A') + 1) * K % p for char in mensaje.upper() if 'A' <= char <= 'Z']
    
    #Se retorna C1 y C2
    return C1, C2


def descifrar(C1, C2, p, a):
    # Se calcula la clave de sesión K usando C1 y la clave privada a
    K = pow(C1, a, p)
    
    # Calcula el inverso modular de K módulo p
    K_inv = pow(K, -1, p)
    
    #Se descifra el mensaje 
    mensaje = ''.join([chr(((char * K_inv) % p - 1) % 26 + ord('A')) for char in C2])
    
    #S e retorna el mensaje descifrado
    return mensaje

def servidor():
    #Se crea un socket para la comunicación 
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #Se enlazar el socket al localhost (127.0.0.1) en el puerto 12345
    server_socket.bind(('localhost', 12345))
    
    #Se espera la conexión 
    server_socket.listen(1)
    
    # Imprimir un mensaje indicando que el servidor está esperando una conexión del cliente
    print("Esperando la conexión del cliente...")

    #Se acepta la conexión 
    connection, client_address = server_socket.accept()
    
    # Imprimir un mensaje indicando que la conexión se ha establecido con la dirección del cliente
    print("Conexión establecida con:", client_address)

    #Se generan las claves p, g, a, A para el intercambio de ellas
    p, g, a, A = generar_claves()
    
    #Se le envia al cliente las claves p, g, A codificadas como cadena de texto
    connection.sendall(f"{p},{g},{A}".encode())

    # Recibir el mensaje cifrado del cliente
    mensaje_cliente = connection.recv(1024).decode()
    
    # Imprimir el mensaje recibido del cliente
    print("Mensaje recibido del cliente:", mensaje_cliente)

    # Cifrar el mensaje recibido utilizando las claves generadas y enviar las componentes cifradas al cliente
    C1, C2 = cifrar(mensaje_cliente, p, g, A)
    connection.sendall(f"{C1},{','.join(map(str, C2))}".encode())

    #Se descifrar el mensaje cifrado y se guarda en un archivo llamado mensajerecibido.txt
    mensaje_descifrado = descifrar(C1, C2, p, a)
    with open('mensajerecibido.txt', 'w') as archivo_recibido:
        archivo_recibido.write(mensaje_descifrado)

    # Cerrar la conexión con el cliente
    connection.close()

if __name__ == "__main__":
    servidor()



