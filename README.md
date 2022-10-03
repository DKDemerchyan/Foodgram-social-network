# Foodgram

![Python](https://img.shields.io/badge/Python-3776AB?style=plastic&logo=python&logoColor=3776AB&labelColor=C0C0C0)
![Django ](https://img.shields.io/badge/Django-092E20?style=plastic&logo=Django&logoColor=092E20&labelColor=C0C0C0)
![Django REST Framework](https://img.shields.io/badge/Django-REST_Framework-092E20?style=plastic&logo=Django&logoColor=092E20&labelColor=C0C0C0)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=plastic&logo=Docker&logoColor=2496ED&labelColor=C0C0C0)
![Postgres](https://img.shields.io/badge/PostgreSQL-4169E1?style=plastic&logo=PostgreSQL&logoColor=4169E1&labelColor=C0C0C0)
![Git](https://img.shields.io/badge/Git-F05032?style=plastic&logo=GitHub&logoColor=F05032&labelColor=C0C0C0)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=plastic&logo=GitHub&logoColor=181717&labelColor=C0C0C0)
![Yandex_Cloud](https://img.shields.io/badge/Yandex-Cloud-87CEFA?style=plastic&labelColor=C0C0C0)
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=plastic&logo=Ubuntu&logoColor=E95420&labelColor=C0C0C0)
![NGINX](https://img.shields.io/badge/NGINX-009639?style=plastic&logo=NGINX&logoColor=009639&labelColor=C0C0C0)
![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?style=plastic&logo=Gunicorn&logoColor=499848&labelColor=C0C0C0)
![.ENV](https://img.shields.io/badge/.ENV-ECD53F?style=plastic&logo=.ENV&logoColor=ECD53F&labelColor=C0C0C0)
___

## Готовый проект можно найти по ссылке [Foodgram](http://84.201.133.116/recipes)

___


## **Сервис позволяет:**
- Публиковать свои рецепты
- Знакомиться с рецептами других пользователей
- Подписываться на других пользователей
- Добавлять рецепты в Избранное
- Формировать список покупок и скачивать его

___

## **Запуск проекта на своем сервере**

### 1. Клонируйте репозиторий на локальную машину и разверните виртуальное окружение в папку /backend/

```
git clone git@github.com:DKDemerchyan/foodgram-project-react.git
```

- [X] *Убедитесь, что у Вас установлен pip*
```
py -m ensurepip --upgrade
```

- [X] *Перейдите в папку /backend/*
```
python -m venv venv
cd foodgram
pip install -r requirements.txt
```

### 2. Подготовьте в папке infra/ файл .env
```
touch .env
```
- [x] Внесите в него 
```
DB_ENGINE=django.db.backends.postgresql_psycopg2
DB_NAME=postgres            <имя базы данных>
POSTGRES_USER=postgres      <пользователь>
POSTGRES_PASSWORD=postgres  <пароль>
DB_HOST=db
DB_PORT=5432
```
### 3. Создайте сервер

*Это можно сделать с помощью сервиса [Yandex.Cloud](https://cloud.yandex.ru/)*. Разверните машину на Ubuntu.

- [x] Обновите индекс пакетов APT и установленные в системе пакеты
```
sudo apt update
sudo apt upgrade -y
```

- [x] Установите:
  - Менеджер пакетов ```pip```
  - Утилиту для создания виртуального окружения ```venv```
  - Систему контроля версий ```git```
```
sudo apt install python3-pip python3-venv git -y
```

- [x] Подготовьте сервер для БД PostgreSQL
```
sudo dpkg-reconfigure locales
```
- В открывшемся интерфейсе найдите локаль ru_RU.UTF-8 и отметьте её, нажав ```пробел```. Затем с помощью клавиши ```Tab``` переместитесь до кнопки Ок и нажмите ```Enter```
- В следующем окне укажите локаль по умолчанию: выберите ru_RU.UTF-8 и снова нажмите ```Enter```.
- Теперь перезапустите сервер и проверьте локаль. 
  ```
  sudo reboot
  locale
  ```

- [x] Установка PostgreSQL
```
sudo apt update 
sudo apt install postgresql postgresql-contrib -y 
```

### 4. Запуск
- [x] Из директории infra/ запустите:
```
scp docker-compose.yml <username>@<host>:/home/<username>/
scp nginx.conf <username>@<host>:/home/<username>/
scp .env <username>@<host>:/home/<username>/
```

- [x] Установите Docker :whale2: и Docker-compose
```
sudo apt install docker.io 
sudo apt install docker-compose
```

- [x] Соберите контейнер и выполните миграции:
```
sudo docker-compose up -d --build
sudo docker-compose exec backend python manage.py migrate
```

- [x] Наполните сервер данными и соберите статику:
```
sudo docker-compose exec backend python manage.py createsuperuser
sudo docker-compose exec backend python manage.py collectstatic --no-input
sudo docker-compose exec backend python manage.py load_ingredients
sudo docker-compose exec backend python manage.py load_tags
```

### Готово, открывайте Ваш сайт и публикуйте рецепты. Приятного аппетита! :yum: