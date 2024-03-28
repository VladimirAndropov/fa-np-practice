import os
import shutil
import json
import socket

DEFAULT_PORT = 9090
DEFAULT_IP = "127.0.0.1"
END_MESSAGE_FLAG = "CRLF_"
MAIN_STORAGE_DIR = "server_storage"


class Server:
    def __init__(self, port_number: int) -> None:
        self.port_number = port_number
        self.sock = None
        self.start_server()

    def start_server(self):
        """Запуск сервера"""
        ip, port = DEFAULT_IP, self.port_number
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((ip, port))
        sock.listen(1)
        print(f"Сервер запущен на {ip}:{port}")

        while True:
            conn, addr = sock.accept()
            print(f"Установлено соединение с клиентом {addr}")
            self.handle_client(conn)

    def handle_client(self, conn):
        """Обработка запросов клиента"""
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break

            command, *args = data.split()

            if command == "list":
                file_list = self.list_files()
                conn.send(json.dumps(file_list).encode())

            elif command == "mkdir" and args:
                result = self.create_directory(args[0])
                conn.send(result.encode())

            elif command == "rmdir" and args:
                result = self.remove_directory(args[0])
                conn.send(result.encode())

            elif command == "rmfile" and args:
                result = self.remove_file(args[0])
                conn.send(result.encode())

            elif command == "rename" and len(args) == 2:
                result = self.rename_file(args[0], args[1])
                conn.send(result.encode())

            elif command == "copyto" and len(args) == 2:
                result = self.copy_to_server(args[0], args[1])
                conn.send(result.encode())

            elif command == "copyfrom" and len(args) == 2:
                result = self.copy_from_server(args[0], args[1])
                conn.send(result.encode())

            elif command == "readfile" and args:
                result = self.read_file(args[0])
                conn.send(result.encode())

            elif command == "exit":
                conn.close()
                break

    def list_files(self):
        """Получить список файлов и папок в рабочей директории"""
        return os.listdir(MAIN_STORAGE_DIR)

    def create_directory(self, dir_name):
        """Создать новую папку"""
        try:
            os.mkdir(os.path.join(MAIN_STORAGE_DIR, dir_name))
            return "Directory created successfully."
        except FileExistsError:
            return "Directory already exists."
        except Exception as e:
            return f"Error creating directory: {str(e)}"

    def remove_directory(self, dir_name):
        """Удалить папку"""
        try:
            shutil.rmtree(os.path.join(MAIN_STORAGE_DIR, dir_name))
            return "Directory removed successfully."
        except FileNotFoundError:
            return "Directory not found."
        except Exception as e:
            return f"Error removing directory: {str(e)}"

    def remove_file(self, file_name):
        """Удалить файл"""
        try:
            os.remove(os.path.join(MAIN_STORAGE_DIR, file_name))
            return "File removed successfully."
        except FileNotFoundError:
            return "File not found."
        except Exception as e:
            return f"Error removing file: {str(e)}"

    def rename_file(self, old_name, new_name):
        """Переименовать файл"""
        try:
            os.rename(
                os.path.join(MAIN_STORAGE_DIR, old_name),
                os.path.join(MAIN_STORAGE_DIR, new_name),
            )
            return "File renamed successfully."
        except FileNotFoundError:
            return "File not found."
        except Exception as e:
            return f"Error renaming file: {str(e)}"

    def copy_to_server(self, local_path, server_path):
        """Скопировать файл с клиента на сервер"""
        try:
            with open(local_path, "rb") as fsrc:
                with open(os.path.join(MAIN_STORAGE_DIR, server_path), "wb") as fdst:
                    shutil.copyfileobj(fsrc, fdst)
            return "File copied to server successfully."
        except FileNotFoundError:
            return "File not found on client."
        except Exception as e:
            return f"Error copying file to server: {str(e)}"

    def copy_from_server(self, server_path, local_path):
        """Скопировать файл с сервера на клиент"""
        try:
            with open(os.path.join(MAIN_STORAGE_DIR, server_path), "rb") as fsrc:
                with open(local_path, "wb") as fdst:
                    shutil.copyfileobj(fsrc, fdst)
            return "File copied from server successfully."
        except FileNotFoundError:
            return "File not found on server."
        except Exception as e:
            return f"Error copying file from server: {str(e)}"

    def read_file(self, file_name):
        """Прочитать содержимое файла"""
        try:
            with open(os.path.join(MAIN_STORAGE_DIR, file_name), "r") as f:
                return f.read()
        except FileNotFoundError:
            return "File not found."
        except Exception as e:
            return f"Error reading file: {str(e)}"


def main():
    server = Server(DEFAULT_PORT)


if __name__ == "__main__":
    main()