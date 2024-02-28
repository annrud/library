# library

### Описание
API для работы с библиотекой **library**.


### Технологии:
- Python 3.10
- Django 5.0.2
- Django REST Framework 3.14.0
- PostgreSQL 12.4
- Docker Compose 3.8
- Gunicorn 21.2.0
- Nginx 1.25.1

### Этапы запуска приложения на локальной машине:
1. Установите <a href=https://docs.docker.com/engine/install/ubuntu/>docker</a>
2. Клонируйте проект в рабочую директорию:<br> 
```$ git clone https://github.com/<ваш_username>/library.git```
3. Создайте файл **_.env_** (в директории рядом с settings.py) с переменными окружения (см. **_.env.dist_**).<br>
4. Создание сервисов (выполнение команды из корневой папки):<br>
```$ docker compose -f infra/docker-compose.yml build```<br>
5. Сборка и запуск контейнеров:<br>
```$ docker compose -f infra/docker-compose.yml up -d```<br>
6. Вход внутрь контейнера backend и выполнение миграций:<br>
```$ docker-compose -f infra/docker-compose.yml exec backend sh```
```# python manage.py migrate```<br>
7. Спецификация: <br>
   - OpenAPI: http://127.0.0.1/api/v1/schema/swagger-ui/ <br>
   - redoc: http://127.0.0.1/api/v1/schema/redoc/ <br>

### Дополнительные команды:<br>
Остановка и удаление контейнеров: ```docker compose -f infra/docker-compose.yml down```<br>
Просмотр логов: ```docker compose -f infra/docker-compose.yml logs```<br>

### Разработчик:
<a href="https://github.com/annrud">*Попова Анна*</a>
