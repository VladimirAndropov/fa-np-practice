#Модифицируйте код клиента таким образом, чтобы он читал строки в цикле до тех пор,
# пока клиент не введет “exit”. Можно считать, что это команда разрыва соединения со стороны клиента.
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