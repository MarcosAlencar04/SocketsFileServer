import socket
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

SERVER_IP = 'localhost'  # IP fixo do servidor
SERVER_PORT = 12345

def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))
    return client_socket

def fetch_server_files():
    client_socket = connect_to_server()
    client_socket.sendall(b'download')
    
    files = client_socket.recv(4096).decode('utf-8').split('\n')
    client_socket.close()
    return files

def upload_file():
    client_socket = connect_to_server()
    client_socket.sendall(b'upload')

    filename = filedialog.askopenfilename()
    if filename:
        client_socket.sendall(os.path.basename(filename).encode('utf-8'))
        with open(filename, 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                client_socket.sendall(data)
        messagebox.showinfo("Info", "Arquivo enviado com sucesso")
    client_socket.close()

def download_file():
    files = fetch_server_files()
    if files:
        download_window = tk.Toplevel(app)
        download_window.title("Selecione um arquivo para download")

        tk.Label(download_window, text="Selecione um arquivo:").pack(pady=5)

        selected_file = tk.StringVar()
        file_combobox = ttk.Combobox(download_window, textvariable=selected_file, values=files)
        file_combobox.pack(pady=5)

        def confirm_download():
            client_socket = connect_to_server()
            client_socket.sendall(b'download')
            client_socket.sendall(selected_file.get().encode('utf-8'))
            save_path = os.path.join('ArquivosCliente', selected_file.get())
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            with open(save_path, 'wb') as f:
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    f.write(data)
            messagebox.showinfo("Info", "Arquivo recebido com sucesso")
            client_socket.close()
            download_window.destroy()

        download_button = tk.Button(download_window, text="Download", command=confirm_download)
        download_button.pack(pady=5)

app = tk.Tk()
app.title("Cliente")

upload_button = tk.Button(app, text="Upload de Arquivo", command=upload_file)
upload_button.pack(pady=10)

download_button = tk.Button(app, text="Download de Arquivo", command=download_file)
download_button.pack(pady=10)

app.mainloop()
