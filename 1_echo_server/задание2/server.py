#Задание 3-Модифицируйте код сервера таким образом, чтобы при разрыве
# соединения клиентом он продолжал слушать данный порт и, таким образом, был доступен для повторного подключения.
import socket

sock = socket.socket()
sock.bind(('', 9090))
sock.listen(1)

while True:
    conn, addr = sock.accept()
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.send(data.upper())
    except ConnectionResetError:
        print("Подключение было разорвано со стороны клиента")
    finally:
        conn.close()

