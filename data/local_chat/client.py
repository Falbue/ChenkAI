import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import socket
import threading
import os

# Создаем окно приложения
window = tk.Tk()
window.title("Chat")
window.geometry("400x700")

with open('data/local_chat/data.txt', 'r') as file:
    ip_address = file.read()
os.remove("data/local_chat/data.txt")
# Создаем поле для отображения сообщений
messages_area = ScrolledText(window)
messages_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Создаем поле для ввода сообщения
entry_field = tk.Entry(window)
entry_field.pack(padx=10, pady=10, fill=tk.X)

# Создаем сокет клиента
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ip_address, 12345))

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
        except ConnectionResetError:
            messages_area.insert(tk.END, "Сервер отключен" + '\n')
            client_socket.close()
            break
        try:
            messages_area.insert(tk.END, message + '\n')
            messages_area.see(tk.END)
        except Exception as e:
            print("Ошибка" + e)
# Запускаем поток для приема сообщений
threading.Thread(target=receive_messages).start()

def send_message(event=None):
    # Отправляем сообщение на серверч
    message = entry_field.get()
    client_socket.sendall(message.encode())
    entry_field.delete(0, tk.END)

# Привязываем событие нажатия Enter к функции отправки сообщения
entry_field.bind('<Return>', send_message)

# Создаем кнопку для отправки сообщения
send_button = tk.Button(window, text="Отправить", command=send_message)
send_button.pack(padx=10, pady=10)

def exit(x):
    client_socket.sendall(x.encode())
    window.destroy()

window.protocol("WM_DELETE_WINDOW", lambda: exit("/close"))

# Запускаем главный цикл обработки событий
window.mainloop()