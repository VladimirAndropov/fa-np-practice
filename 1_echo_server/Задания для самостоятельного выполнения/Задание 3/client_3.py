#Модифицируйте код сервера таким образом,
# чтобы при разрыве соединения клиентом он продолжал слушать
# данный порт и, таким образом, был доступен для повторного подключения.
import socket
sock = socket.socket()
sock.connect(('localhost', 9090))


while True:
    msg = input('Введите сообщение: ')
    if msg != "exit":
        sock.send(f'{msg}'.encode())
        data = sock.recv(1024)
        print(data)
    if msg == "exit":
        print("Разрыв соединения")
        break