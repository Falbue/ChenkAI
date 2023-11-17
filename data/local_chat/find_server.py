import threading
import socket

message = "/login"
open_servers = []

def handle_client(ip_address):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((ip_address, 12345))
        client_socket.sendall(message.encode())
        while True:
            try:
                response = client_socket.recv(1024).decode()
                open_servers.append(f"{response} {ip_address}")
            except:
                print(f"Работа с сервером {ip_address} завершена")
                client_socket.close()
                return  # остановка выполнения функции
            print(f"Ответ сервера {ip_address}: {response}")
            client_socket.close()
            break
    except:
        print(f"Сервер {ip_address} недоступен")
        client_socket.close()
    finally:
        client_socket.close()

threads = []
for port in range (1,256):
    ip_address = f"192.168.0.{port}"
    thread = threading.Thread(target=handle_client, args=(ip_address,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print(open_servers)