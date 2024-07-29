import socket
import os
import threading
from datetime import datetime

LOG_FILE = "server_log.txt"

def log_action(action, client_address, filename):
    with open(LOG_FILE, 'a') as log_file:
        log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {client_address[0]}:{client_address[1]} - {action} - {filename}\n"
        log_file.write(log_entry)
        print(log_entry, end='')

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(5)
    print("Servidor ouvindo na porta 12345")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Conexão de {client_address}")
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

def handle_client(client_socket, client_address):
    try:
        command = client_socket.recv(1024).decode('utf-8').strip()
        if command == 'upload':
            receive_file(client_socket, client_address)
        elif command == 'download':
            send_file(client_socket, client_address)
    except Exception as e:
        print(f"Erro ao processar comando: {e}")
    finally:
        client_socket.close()

def receive_file(client_socket, client_address):
    try:
        filename = client_socket.recv(1024).decode('utf-8').strip()
        save_path = os.path.join('ArquivosServidor', filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        with open(save_path, 'wb') as f:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                f.write(data)
        print(f"Arquivo {filename} recebido")
        log_action("UPLOAD", client_address, filename)
    except Exception as e:
        print(f"Erro ao receber arquivo: {e}")

def send_file(client_socket, client_address):
    try:
        files = os.listdir('ArquivosServidor')
        files_list = "\n".join(files)
        client_socket.sendall(files_list.encode('utf-8'))

        filename = client_socket.recv(1024).decode('utf-8').strip()
        file_path = os.path.join('ArquivosServidor', filename)
        if filename in files:
            with open(file_path, 'rb') as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    client_socket.sendall(data)
            print(f"Arquivo {filename} enviado")
            log_action("DOWNLOAD", client_address, filename)
        else:
            client_socket.sendall(b'File not found')
    except Exception as e:
        print(f"Erro ao enviar arquivo: {e}")

if __name__ == '__main__':
    start_server()

