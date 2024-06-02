# docker-compose

из трех семинаров

- на первом семинаре установить mysql nginx через docker-compose
[Методичка](13_Dockerfile/Методических_материалов_по_темам_«Контейнеризации_и_оркестровки.pdf)

- на втором - установить portainer
[Методичка](https://docs.portainer.io/v/2.20/start/install-ce/server/docker/linux)
- на третьем семинаре создать Dockerfile с приложением из 1_echo_server_ML (читай дальше как)

# создание Dockerfile

качаем Dockerfile из папки server
скачиваем приложение, например
*1_echo_server*

**2 файла: клиент и сервер**

https://github.com/VladimirAndropov/fa-np-practice/blob/main/1_echo_server/server.py

https://github.com/VladimirAndropov/fa-np-practice/blob/main/1_echo_server/client.py

Всё кладем в рабочий каталог где лежит Dockerfile

запускаем сборку контейнера

```
docker build .
```

Выпадет ошибка, что нет файла requirements.txt

Создадим этот файл и впишем в него пакет который должен быть установлен перед запуском нашего приложения

```
touch requirements.txt
```
добавляем в requirements.txt строку
*imutils*

-  **RUN pip3 install -r requirements.txt** означает установить пакет imutils

Добавляем 2 строки в Dockerfile

```
COPY server.py /app/
COPY client.py /app/
```

- что означает скопировать эти файлы из локальной машины в контейнер папку /app/

Изменяем запуск в последней строке на 

```
CMD ["python3", "./server.py"]
```

Запускаем 

```
docker build .
```

Если контейнер сбилдился, то в консоли в последней строке выскочит строка с именем контейнера 

```
Removing intermediate container b29746f275f4
 ---> d88c8bd383bc
Successfully built d88c8bd383bc
```

**d88c8bd383bc**

Запускаем контейнер

```
sudo docker run -p 9090:9090 d88c8bd383bc
```

Запускам клиент внутри контейнера

```
sudo docker run -it  d88c8bd383bc bash

python3 client.py
```

И на запущеном контейнере с сервером получаем отбивку от сервера

*connected: ('172.17.0.1', 47048)*
