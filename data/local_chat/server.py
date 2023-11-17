import socket
import threading
import os

# Создаем сокет сервера
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = socket.gethostbyname(socket.gethostname())
server_socket.bind((ip_address, 12345))
print(f"Адрес: {ip_address}")
server_socket.listen(5)
try:
    with open('data/local_chat/data.txt', 'r') as file:
        login = file.read()
except:
    login = "test"
# Список подключенных клиентов
clients = []

def handle_client(client_socket, client_address):
    while True:
        # Принимаем сообщение от клиента
        try:
            message = client_socket.recv(1024).decode()
            print(message)
        
            if message == "/close":
                # Если сообщения нет, отключаем клиента
                clients.remove(client_socket)
                client_socket.close()
                print("Отключился...")
                break

            if message == "/login":
                for client in clients:
                    message = login
                    client.sendall(message.encode())
                    clients.remove(client_socket)
                    client_socket.close()
                    print("Поиск окончен")
                    break
            # Отправляем сообщение всем клиентам
            else:
                for client in clients:
                    try:
                        client.sendall(message.encode())
                    except Exception as e:
                        print(e)
                        break
        except Exception as e:
            print("Ошибка на стороне клиента")
            print(e)
            break
while True:
    # Принимаем подключение клиента
    client_socket, client_address = server_socket.accept()
    
    # Добавляем клиента в список
    clients.append(client_socket)
    
    # Запускаем обработчик клиента в отдельном потоке
    threading.Thread(target=handle_client, args=(client_socket, client_address)).start()