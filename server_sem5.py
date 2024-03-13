# import socket
# from typing import Any


# def port_validation(value: Any, check_open: bool = False) -> bool:
#     """Проверка на корректность порта"""
#     try:
#         # Проверка на число
#         value = int(value)
#         # Проверка на диапазон
#         if 1 <= value <= 65535:
#             # Проверка то, занят ли порт
#             if check_open:
#                 return check_port_open(value)
#             print(f"Корректный порт {value}")
#             return True

#         print(f"Некорректное значение {value} для порта")
#         return False

#     except ValueError:
#         print(f"Значение {value} не является числом!")
#         return False


# def check_port_open(port: int) -> bool:
#     """
#     Проверка на свободный порт port

#     Является частью логики port_validation
#     """
#     try:
#         sock = socket.socket()
#         sock.bind(("", port))
#         sock.close()
#         print(f"Порт {port} свободен")
#         return True
#     except OSError:
#         print(f"Порт {port} занят")
#         return False


# def ip_validation(address: str) -> bool:
#     """Проверка на корректность ip-адреса (v4)"""
#     error_message = f"Некорректный ip-адрес {address}"
#     ok_message = f"Корректный ip-адрес {address}"
#     try:
#         socket.inet_pton(socket.AF_INET, address)
#     except AttributeError:  # no inet_pton here, sorry
#         try:
#             socket.inet_aton(address)
#         except socket.error:
#             print(error_message)
#             return False
#         return address.count(".") == 3
#     except socket.error:  # not a valid address
#         print(error_message)
#         return False

#     print(ok_message)
#     return True
from ctypes import pythonapi
from multiprocessing import process
import socket


pythonapi
PORT = 9090
 
sock = socket.socket()
sock.bind(('', PORT))
sock.listen()
 
while True:
    print("Слушаем порт", PORT)
    conn, addr = sock.accept()
    print(addr)
    
    request = conn.recv(1024).decode()
    print(request)
    
    response = process(request)
    conn.send(response.encode())
 
sock.close()

HOST = 'localhost'
PORT = 9090
 
while True:
    sock = socket.socket()
    sock.connect((HOST, PORT))
    
    request = input('myftp@shell$ ')
    sock.send(request.encode())
    
    response = sock.recv(1024).decode()
    print(response)
    
    sock.close()

def process(req):
    if req == 'pwd':
        return os.getcwd()
    elif req == 'ls':
        return '; '.join(os.listdir())
    else:
        return 'bad request'
