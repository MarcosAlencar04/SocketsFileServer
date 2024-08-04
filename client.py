import socket
import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk

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
        download_window = tk.Toplevel(app)
        download_window.title("Selecione um arquivo para download")

        # Centralizar a janela de download
        window_width = 300
        window_height = 150
        screen_width = app.winfo_screenwidth()
        screen_height = app.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        download_window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

        tk.Label(download_window, text="Selecione um arquivo:").pack(pady=5)

        selected_file = tk.StringVar()
        file_combobox = ttk.Combobox(download_window, textvariable=selected_file, values=files)
        file_combobox.pack(pady=5)

        def confirm_download(selected_file, client_socket):
            if selected_file:
                file_name = selected_file.get()
                client_socket.sendall(file_name.encode())
                save_path = os.path.join("ArquivosCliente", file_name)
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                with open(save_path, 'wb') as f:
                    while True:
                        data = client_socket.recv(1024)
                        if not data:
                            break
                        f.write(data)
                messagebox.showinfo("Info", "Arquivo recebido com sucesso")
                download_window.destroy()
        
        download_button = tk.Button(download_window, text="Download", command=lambda: confirm_download(selected_file, client_socket))
        download_button.pack(pady=5)

def show_main_window(server_ip):
    global app
    app = tk.Tk()
    app.title("Cliente")

    # Ajustar tamanho da janela principal e centralizar botões
    window_width = 300
    window_height = 150
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    app.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    frame = tk.Frame(app)
    frame.pack(expand=True)

    upload_button = tk.Button(frame, text="Upload de Arquivo", command=lambda: upload_file(server_ip))
    upload_button.pack(pady=10)

    download_button = tk.Button(frame, text="Download de Arquivo", command=lambda: download_file(server_ip))
    download_button.pack(pady=10)

    app.mainloop()

def main():
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal temporária

    server_ip = simpledialog.askstring("IP do Servidor", "Digite o IP do servidor:")
    if server_ip:
        root.destroy()  # Fecha a janela temporária
        show_main_window(server_ip)

if __name__ == "__main__":
    main()
