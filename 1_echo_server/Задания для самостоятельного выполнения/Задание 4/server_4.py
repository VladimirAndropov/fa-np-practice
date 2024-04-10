#Модифицируйте код клиента и сервера таким образом,
# чтобы номер порта и имя хоста (для клиента) они спрашивали у пользователя.
# Реализовать безопасный ввод данных и значения по умолчанию.

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