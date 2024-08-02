import socket
import os

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(5)
    print("Servidor ouvindo na porta 12345")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Conexão de {client_address}")

        command = client_socket.recv(1024).decode()

        if command == 'upload':
            receive_file(client_socket)
        elif command == 'download':
            send_file(client_socket)

        client_socket.close()

def receive_file(client_socket):
    filename = client_socket.recv(1024).decode()
    save_path = os.path.join("ArquivosServidor", filename)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, 'wb') as f:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            f.write(data)
    print(f"Arquivo {filename} recebido e salvo em {save_path}")

def send_file(client_socket):
    files = os.listdir("ArquivosServidor")
    files_list = "\n".join(files)
    client_socket.sendall(files_list.encode())

    filename = client_socket.recv(1024).decode()
    file_path = os.path.join("ArquivosServidor", filename)
    if filename in files:
        with open(file_path, 'rb') as f:
            while (data := f.read(1024)):
                client_socket.sendall(data)
        print(f"Arquivo {filename} enviado")
    else:
        client_socket.sendall(b'File not found')

if __name__ == '__main__':
    start_server()
