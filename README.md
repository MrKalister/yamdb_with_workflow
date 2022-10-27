# REST API Yamdb – база отзывов пользователей о медиа произведениях-книги,фильмы,музыка.
![Build Status](https://github.com/MrKalister/yamdb_with_workflow/actions/workflows/yamdb_workflow.yml/badge.svg)
## Технологический стек:
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=56C0C0&color=008080)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=008080)](https://www.postgresql.org/)
[![JWT](https://img.shields.io/badge/-JWT-464646?style=flat&color=008080)](https://jwt.io/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat&logo=NGINX&logoColor=56C0C0&color=008080)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=gunicorn&logoColor=56C0C0&color=008080)](https://gunicorn.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker Hub](https://img.shields.io/badge/-Docker%20Hub-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/products/docker-hub)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat&logo=GitHub%20actions&logoColor=56C0C0&color=008080)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat&logo=Yandex.Cloud&logoColor=56C0C0&color=008080)](https://cloud.yandex.ru/)

## Возможности Workflow
* tests - Проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8) и запуск pytest. Дальнейшие шаги выполнятся только если push был в ветку master или main.
* build_image_and_push_to_docker_hub - Сборка и отправка докер-образов на Docker Hub
* deploy - Автоматический деплой проекта на боевой сервер. Выполняется копирование файлов из репозитория на сервер:
* send_message - Отправка уведомления в Telegram

### Подготовительные процедуры для запуска workflow
1. Создайте и активируйте виртуальное окружение, обновите pip:
```
python3 -m venv venv
source venv/Scripts/activate
python3 -m pip install --upgrade pip
```
2. Запустите автотесты:
```
pytest
```
3. Скопируйте подготовленные файл `docker-compose.yaml` и папку `nginx` с конфигурацией из вашего проекта на сервер:
```
scp docker-compose.yaml <username>@<host>:/home/<username>/docker-compose.yaml
scp -r nginx <username>@<host>:/home/<username>/
```
4. В репозитории на Гитхабе добавьте данные в `Settings - Secrets - Actions secrets`:
```
DOCKER_USERNAME - имя пользователя в DockerHub
DOCKER_PASSWORD - пароль пользователя в DockerHub
HOST - ip-адрес сервера
USER - пользователь на сервере
SSH_KEY - приватный ssh-ключ (публичный должен быть на сервере)
PASSPHRASE - кодовая фраза для ssh-ключа(если создавалась)
DB_ENGINE - django.db.backends.postgresql
DB_NAME - postgres (по умолчанию)
POSTGRES_USER - postgres (по умолчанию)
POSTGRES_PASSWORD - 12345 (по умолчанию)
DB_HOST - db
DB_PORT - 5432
SECRET_KEY - секретный ключ приложения django (необходимо чтобы были экранированы или отсутствовали скобки)
TELEGRAM_TO - id своего телеграм-аккаунта (можно узнать у @userinfobot, команда /start)
TELEGRAM_TOKEN - токен бота (получить токен можно у @BotFather, /token, имя бота)
```
При внесении изменений и выполнения команд:
```
git add .
git commit -m "..."
git push
```
Автоматически выполняется блок команд jobs (см. Возможности Workflow)

## Описание проекта:
Реализован пользовательский функционал дающий возможность пользоваться приложением не посещая сайт:
1.	Пользовательские роли:
   * Аноним — может просматривать описания произведений, читать отзывы и комментарии.
   * Аутентифицированный пользователь (user)— может читать всё, как и Аноним, дополнительно может публиковать отзывы и ставить рейтинг произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы и ставить им оценки; может редактировать и удалять свои отзывы и комментарии.
   * Модератор (moderator) — те же права, что и у Аутентифицированного пользователя плюс право удалять и редактировать любые отзывы и комментарии.
   * Администратор (admin) — полные права на управление проектом и всем его содержимым. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
   * Администратор Django — те же права, что и у роли Администратор.
2.	Система регистрации пользователей:
   * Пользователь отправляет POST-запрос с параметром email на /api/v1/auth/email/.
   * YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email.
   * Пользователь отправляет POST-запрос с параметрами email и confirmation_code на /api/v1/auth/token/, в ответе на запрос ему приходит token(JWT-токен).
   * После регистрации и получения токена пользователь может отправить PATCH-запрос на /api/v1/users/me/ и заполнить поля в своём профайле.
3.	Ресурсы API YaMDb:
   * Ресурс AUTH: аутентификация.
   * Ресурс USERS: пользователи.
   * Ресурс TITLES: произведения, к которым можно написать отзыв.
   * Ресурс CATEGORIES: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
   * Ресурс GENRES: жанры произведений.
   * Ресурс REVIEWS: отзывы на произведения.
   * Ресурс COMMENTS: комментарии к отзывам.

## Как развернуть проект локально:

Все команды выполняются в командной строке.
1. Клонируйте репозиторий:
* Вариант 1. По SSH:
```
git clone git@github.com:MrKalister/yamdb_final.git
```
* Вариант 2. По HTTPS:
```
git clone https://github.com/MrKalister/yamdb_final.git
```
2. Перейдите в папку для развертывания:
```
cd yamdb_final/infra
```
3. Добавьте пользователя в группу docker:
Данное шаг можно пропустить, в таком случае в начале каждой команды необходимо указывать "sudo"
```
sudo usermod -aG docker username
```
4. Убедитесь что пользователь добавлен в группу:
```
groups
```
5. Заполнить шаблон .env_example:
Лучше всего воспользоваться встроенным редактором nano или любым аналогичным.
```
nano .env_example
```
6. Заполнить секретными данными:
```
DB_ENGINE=django.db.backends.postgresql # база данных
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=12345 # пароль для подключения к базе данных
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
SECRET_KEY=12345 # секретный ключ от проекта Django
```
7. Переименовать env-файл:
```
cp .env_example .env
```
8. В папке проекта создайте образ:
Укажите username вашего акаунта на DockerHub, название образа и тег(опционально).
```
docker build -t <username>/<imagename>:<tag>.
```
9. Соберите контейнеры:
```
docker-compose -f infra/docker-compose.yaml up -d --build
```
или пересоберите:
```
docker-compose up -d --build
```
10. Войдите в контейнер:
```
docker-compose exec web bash
```
10. Выполните миграции:
```
python manage.py makemigrations
python manage.py migrate
```
11. Создайте суперпользователя:
```
python manage.py createsuperuser
```

## Как развернуть проект на сервере:
1. Установите соединение с сервером:
```
ssh username@server_address
```
2. Добавьте пользователя в группу docker:
Данное шаг можно пропустить, в таком случае в начале каждой команды необходимо указывать "sudo"
```
sudo usermod -aG docker username
```
3. Установите Docker и Docker-compose:
```
apt install docker.io
apt-get update
apt-get install docker-compose-plugin
apt install docker-compose
docker-compose version
```
4. Создайте на локальном машине конфигурацию `nginx` и перенесите на сервер:
```
scp -r nginx username@51.250.110.135:/home/username/
```
5. Создайте на локальном машине файл `docker-compose.yaml` и перенесите на сервер:
```
scp docker-compose.yaml username@51.250.110.135:/home/username/
```

### После успешного деплоя:
1. Отобразите список работающих контейнеров:
```
sudo docker container ls -a
```
2. В списке контейнеров копируйте CONTAINER ID контейнера username/api_yamdb:latest (username - имя пользователя на DockerHub).   
Выполните вход в контейнер:
```
sudo docker exec -it <CONTAINER_ID> bash
```
3. Внутри контейнера выполните миграции:
```
python manage.py makemigrations
python manage.py migrate
```
4. Создайте суперпользователя:
```
python manage.py createsuperuser
```
Документация к API доступна по адресу http://ip_adress/redoc/
Для доступа к документации её необходимо скопировать в папку статики:
```
cp redoc.yaml static/
```
API доступен по адресу [http://ip_adress/api/v1/]
