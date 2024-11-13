import socket

# Crear un socket TCP (SOCK_STREAM)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al servidor en localhost y puerto 8080
client_socket.connect(('localhost', 8080))

# Recibir el mensaje del servidor
data = client_socket.recv(1024)
print(f"Recibido del servidor: {data.decode()}")

# Enviar un mensaje al servidor
client_socket.send(b"Hola, servidor! Soy el cliente.")

# Cerrar la conexión
client_socket.close()
