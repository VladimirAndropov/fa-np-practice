import json
import logging
import socket
import threading
import struct

from cli_validator import port_validation, ip_validation

DEFAULT_PORT = 9090
DEFAULT_IP = "127.0.0.1"
END_MESSAGE_FLAG = "CRLF"

# Настройки логирования
logging.basicConfig(
    format="%(asctime)-15s [%(levelname)s] %(funcName)s: %(message)s",
    handlers=[logging.FileHandler("./logs/client.log")],
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


class Client:
    def __init__(self, server_ip: str, port_number: int) -> None:
        self.server_ip = server_ip
        self.port_number = port_number
        self.sock = None
        self.new_connection()

        # Авторизуемся
        self.send_auth()

        # Поток чтения данных от сервера
        t = threading.Thread(target=self.read_message)
        t.daemon = True
        t.start()

        # Работа с данными, поступающими от пользователя
        self.user_processing()

    def new_connection(self):
        """Осуществляет новое соединение по сокету"""

        ip, port = self.server_ip, self.port_number
        sock = socket.socket()
        sock.setblocking(1)
        sock.connect((ip, port))
        self.sock = sock
        logging.info(f"Успешное соединение с сервером {ip}:{port}")

    def send_reg(self, password):
        """Логика регистрации пользователя в системе"""
        print("*Новая регистрация в системе*")
        while True:
            input_username = input("Введите ваше имя пользователя (ник) -> ")
            if input_username == "":
                print("Имя пользователя не может быть пустым!")
            else:
                data = json.dumps(
                    {"password": password, "username": input_username},
                    ensure_ascii=False,
                )
                self.sock.send(data.encode())
                logger.info(f"Отправка данных серверу: '{data}'")

                # Получаем данные с сервера
                response = json.loads(self.sock.recv(1024).decode())
                if not response["result"]:
                    raise ValueError(
                        f"Не удалось осуществить регистрацию, ответ сервера {response}, более подробно см логи сервера"
                    )
                logger.info("Успешно зарегистрировались")
                break

    def send_auth(self):
        """Логика авторизации клиента"""
        login_iter = 1
        while True:

            # Отдельные строки для объяснения механизма авторизации при первом входе
            req_password_str = "Введите пароль авторизации"
            req_password_str += (
                "\nЕсли это ваш первый вход в систему, то он будет использоваться для последующей авторизации в системе -> "
                if login_iter == 1
                else " -> "
            )

            user_password = input(req_password_str)
            if user_password != "":

                data = json.dumps({"password": user_password}, ensure_ascii=False)
                # Отправляем сообщение
                self.sock.send(data.encode())
                logger.info(f"Отправка данных серверу: '{data}'")

                # Получаем данные с сервера
                response = json.loads(self.sock.recv(1024).decode())

                # Если успешно авторизовались
                if response["result"]:
                    print(
                        "Авторизация прошла успешно, можете вводить сообщения для отправки:"
                    )
                    break

                # Если авторизация не удалась
                elif response["description"] == "wrong auth":
                    print("Неверный пароль!")
                    # Делаем новое соединение
                    # т.к. сервер рвет соединение, если авторизация не удалась
                    self.new_connection()

                # Если это первый вход с таким ip-адресом, то необходима регистрация
                elif response["description"] == "registration required":
                    self.new_connection()
                    self.send_reg(user_password)
                    self.new_connection()

                else:
                    raise ValueError(
                        f"Получили неожиданный ответ от сервера: {response}"
                    )

            else:
                print("Пароль не может быть пустым")

            login_iter += 1

    def receive_message(self):
        """Прием текстового сообщения с заголовком длины"""
        # Получаем заголовок фиксированной длины (4 байта)
        header = self.sock.recv(4)
        # Распаковываем заголовок, чтобы получить длину сообщения
        message_length = struct.unpack('!I', header)[0]
        # Получаем сообщение с учетом длины
        message = self.sock.recv(message_length).decode('utf-8')
        return message

    def read_message(self):
        """Чтение сообщения"""
        while True:
            data = receive_message(self.sock)
            if data:
                logger.info(f"Прием данных от сервера: '{data}'")
                data = json.loads(data)
                message_text, user_name = data["text"], data["username"]

                print(f"[{user_name}] {message_text}")

    def send_message(self, message: str):
        """Отправка сообщения"""

        # Добавляем флаг конца сообщения (по-другому я не знаю как передавать больше 1024 и не разрывать соединение)
        message += END_MESSAGE_FLAG

        # Отправляем сообщение
        self.sock.send(message.encode())
        logger.info(f"Отправка данных серверу: '{message}'")

    # В методе Client.user_processing() пользователь может отправлять несколько сообщений подряд.
    def user_processing(self):
        """Обработка ввода сообщений пользователя"""
        while True:
            msg = input()
            # Если сообщение exit
            if msg == "exit":
                break

    def __del__(self):
        if self.sock:
            self.sock.close()
        logger.info("Разрыв соединения с сервером")


def main():
    # Запрос порта у пользователя
    port_input = input("Введите номер порта сервера -> ")
    # Проверка корректности введенного порта
    port_flag = port_validation(port_input)
    if not port_flag:
        port_input = DEFAULT_PORT
        print(f"Выставили порт {port_input} по умолчанию")

    # Запрос IP-адреса сервера у пользователя
    ip_input = input("Введите ip-адрес сервера -> ")
    # Проверка корректности введенного IP-адреса
    ip_flag = ip_validation(ip_input)
    if not ip_flag:
        ip_input = DEFAULT_IP
        print(f"Выставили ip-адрес {ip_input} по умолчанию")

    # Создание клиента с указанными параметрами
    client = Client(ip_input, int(port_input))


if __name__ == "__main__":
    main()
