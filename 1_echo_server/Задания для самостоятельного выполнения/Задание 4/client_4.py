#Модифицируйте код клиента и сервера таким образом, чтобы номер порта и имя хоста
# (для клиента) они спрашивали у пользователя. Реализовать безопасный ввод данных и значения по умолчанию.
import socket
sock = socket.socket()

while True:
    msg = input('Введите сообщение: ')
    if msg != "exit":
        sock.send(f'{msg}'.encode())
        data = sock.recv(1024)
        print(data)
    if msg == "exit":
        print("Разрыв соединения")
        break