import socket
import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

def connect_to_server(server_ip):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, 12345))
    return client_socket

def upload_file(server_ip):
    client_socket = connect_to_server(server_ip)
    client_socket.sendall(b'upload')

    filename = filedialog.askopenfilename()
    if filename:
        client_socket.sendall(os.path.basename(filename).encode())
        with open(filename, 'rb') as f:
            while (data := f.read(1024)):
                client_socket.sendall(data)
        messagebox.showinfo("Info", "Arquivo enviado com sucesso")
    client_socket.close()

def download_file(server_ip):
    client_socket = connect_to_server(server_ip)
    client_socket.sendall(b'download')

    files = client_socket.recv(4096).decode().split('\n')
    if files:
        selected_file = simpledialog.askstring("Escolher arquivo", f"Arquivos disponíveis:\n{'\n'.join(files)}\n\nDigite o nome do arquivo:")
        if selected_file:
            client_socket.sendall(selected_file.encode())
            save_path = os.path.join("ArquivosCliente", selected_file)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, 'wb') as f:
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    f.write(data)
            messagebox.showinfo("Info", "Arquivo recebido com sucesso")
    client_socket.close()

app = tk.Tk()
app.title("Cliente")

server_ip = simpledialog.askstring("IP do Servidor", "Digite o IP do servidor:")

upload_button = tk.Button(app, text="Upload de Arquivo", command=lambda: upload_file(server_ip))
upload_button.pack(pady=10)

download_button = tk.Button(app, text="Download de Arquivo", command=lambda: download_file(server_ip))
download_button.pack(pady=10)

app.mainloop()
