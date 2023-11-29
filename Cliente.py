import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util.Padding import pad

def cifrar(clave_publica, texto_plano):
    # Crea un objeto cifrador con la clave pública y cifra el texto
    cifrador = PKCS1_OAEP.new(clave_publica)
    texto_cifrado = cifrador.encrypt(texto_plano)
    return texto_cifrado

def main():
    # Crea un socket para el cliente
    socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Conecta al servidor en el puerto 12345
    socket_cliente.connect(('localhost', 12345))

    # Recibe la clave pública del servidor
    clave_publica = RSA.import_key(socket_cliente.recv(4096))

    # Lee el mensaje desde el archivo 'mensajeentrada.txt'
    with open('mensajeentrada.txt', 'r') as archivo:
        mensaje = archivo.read()

    # Cifra el mensaje utilizando la clave pública del servidor
    mensaje_encriptado = cifrar(clave_publica, mensaje.encode())

    # Envía el mensaje encriptado al servidor
    socket_cliente.send(mensaje_encriptado)

    print("Mensaje encriptado enviado al servidor")

    # Cierra el socket del cliente
    socket_cliente.close()

# Llama a la función principal
main()
