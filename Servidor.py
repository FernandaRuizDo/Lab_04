#Fernanda Ruiz y Rayen Lara
import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util.Padding import unpad

def descifrar(clave_privada, texto_cifrado):
    # Crea un objeto cifrador con la clave privada y descifra el texto
    cifrador = PKCS1_OAEP.new(clave_privada)
    texto_plano = cifrador.decrypt(texto_cifrado)
    return texto_plano

def generar_clave_rsa():
    # Genera un par de claves RSA (pública y privada) de 2048 bits
    clave = RSA.generate(2048)
    clave_publica = clave.publickey()
    return clave, clave_publica

def main():
    # Crea un socket para el servidor
    socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Asocia el socket al puerto 12345 y escucha conexiones entrantes
    socket_servidor.bind(('localhost', 12345))
    socket_servidor.listen()

    print("Esperando conexión...")
    # Acepta la conexión del cliente y obtiene el socket del cliente y su dirección
    socket_cliente, direccion = socket_servidor.accept()
    print(f"Conexión establecida con {direccion}")

    # Genera el par de claves RSA
    clave_privada, clave_publica = generar_clave_rsa()

    # Envía la clave pública al cliente
    socket_cliente.send(clave_publica.export_key())

    # Recibe el mensaje encriptado desde el cliente
    mensaje_encriptado = socket_cliente.recv(2048)

    # Descifra el mensaje utilizando la clave privada
    mensaje_desencriptado = descifrar(clave_privada, mensaje_encriptado)
    print(f"Mensaje desencriptado: {mensaje_desencriptado.decode()}")

    # Guarda el mensaje desencriptado en el archivo 'mensajerecibido.txt'
    with open('mensajerecibido.txt', 'w') as archivo:
        archivo.write(mensaje_desencriptado.decode())

    print("Mensaje desencriptado y guardado en 'mensajerecibido.txt'")

    # Cierra los sockets del cliente y del servidor
    socket_cliente.close()
    socket_servidor.close()

# Llama a la función principal
main()
