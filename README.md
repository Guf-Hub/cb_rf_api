# Apache Superset

https://superset.apache.org/docs/installation/pypi
https://developers.sber.ru/docs/ru/sdp/sdpanalytics/guidelines-reports-SDPBI

# PostgreSQL

https://ubuntu.com/server/docs/install-and-configure-postgresql
https://www.linuxscrew.com/postgresql-check-running

```bash
sudo apt update
sudo apt install postgresql
sudo systemctl status postgresql

dpkg -l | grep postgresql

```

# Nginx

https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-20-04
https://timeweb.cloud/tutorials/ubuntu/kak-ustanovit-nginx-na-ubuntu

```bash
sudo apt update
sudo apt install nginx
sudo systemctl enable nginx
sudo service nginx status
sudo systemctl is-enabled nginx
```
Запуск

```bash
  sudo systemctl start nginx
```
Отключение

```bash
sudo systemctl stop nginx
```
Перезапуск

```bash
sudo systemctl restart nginx
```
Перезагрузка

```bash
sudo systemctl reload nginx
```
Проверка состояния службы

```bash
sudo systemctl status nginx
```
Тестирование конфигурации

```bash
sudo nginx -t
```

# Firewall

https://selectel.ru/blog/tutorials/how-to-configure-firewall-with-ufw-on-ubuntu-20/

```bash
sudo apt install ufw
```
```bash
sudo nano /etc/ufw/applications.d/nginx.ini
```

```ini
[Nginx HTTP]
title=Web Server
description=Enable NGINX HTTP traffic
ports=80/tcp

[Nginx HTTPS] \
title=Web Server (HTTPS) \
description=Enable NGINX HTTPS traffic
ports=443/tcp

[Nginx Full]
title=Web Server (HTTP,HTTPS)
description=Enable NGINX HTTP and HTTPS traffic
ports=80,443/tcp
```

```bash
sudo ufw app list
```

```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow 'OpenSSH'
sudo ufw enable
```

```bash
sudo ufw status
```

# Docker

https://github.com/luchanos/luchanos_oxford_university
https://docs.docker.com/desktop/install/linux-install/

```bash
docker-compose -f docker-compose.yaml up -d
```

```bash
docker ps
```

### Список установленных программ диск С Windows

```bash
 wmic product get name > installed_programs.txt
```

### PIP

```bash
pip freeze > requirements.txt
```

# Poetry

[Команды](https://python-poetry.org/docs/basic-usage/)

### First, let’s create our new project, let’s call it poetry-demo

```bash
poetry new <PROJECT NAME>
```

### Инициализация уже существующего проекта

```bash
poetry init
```

### Установка версий

Мы запрашиваем _pendulum_ пакет с ограничением версии ^2.1.

Это означает любую версию, большую или равную 2.1.0, но меньше 3.0.0 (>=2.1.0 <3.0.0).

```bash
poetry add <PACEGE NAME>
```

### Запустить скрипт

```bash
poetry run python <SCRIPT NAME>.py
```

### Активация виртуальной среды

```bash
poetry shell
```

### Установка зависимостей

Чтобы установить определенные зависимости для вашего проекта, просто запустите install команду.

```bash
poetry poetry install <PACKAGES NAME>
```

### Установка только зависимостей

По умолчанию текущий проект устанавливается в редактируемом режиме.

Если вы хотите установить только зависимости, запустите install команду с --no-root флагом:

```bash
poetry install --no-root
```

Команда add добавляет необходимые пакеты в ваш каталог pyproject.toml и устанавливает их.

```bash
poetry poetry add <PACKAGES NAME>
```

### Обновление зависимостей до последних версий

```bash
poetry update
```

### Команда remove удаляет пакет из текущего списка установленных пакетов

```bash
poetry remove <PACKAGES NAME>
```
### В requirements.txt

```bash
poetry export --without-hashes --without dev --format=requirements.txt > requirements.txt
```

# Git

[Команды](https://www.atlassian.com/ru/git/glossary#commands)

Инициализировать новый репозиторий Git

```bash
git init
```

Проверить статус (показывает состояния файлов в рабочем каталоге и индексе: какие файлы изменены, но не добавлены в
индекс; какие ожидают коммита в индексе)

```bash
git status
```

Создать README.md

```bash
git add README.md
```

Добавить файлы (добавляет содержимое рабочего каталога в индекс (staging area) для последующего коммита)

```bash
git add .
```
```bash
git add .gitignore
```
Отменить изменения

```bash
git reset
```

Удаление файлов из индекса и рабочей копии (похожа на git add с тем лишь исключением, что она удаляет, а не добавляет
файлы для следующего коммита)

```bash
git rm
```

Удаление файлов из индекса и рабочей копии !!!

```bash
git rm --cached <file_name>

```

Удаление мусора из рабочего каталога

```bash
git clean
```

Сделать коммит

```bash
git commit -m "first commit"
```

Опубликовать

```bash
git push -u origin main
```

Копировать существующий репозитория Git

```bash
git clone <name>
```

Настройки параметров конфигурации в инсталляции Git

```bash
git config
```

Изучить предыдущие версии проекта

```bash
git log
```

Create a new repository on the command line

```bash
echo "# wbserf" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/Guf-Hub/trendy.git
git push -u origin main
```

Push an existing repository from the command line

```bash
git remote add origin https://github.com/Guf-Hub/wbserf.git
git branch -M main
git push -u origin main
```

# Установить время на сервере

```bash
sudo timedatectl set-timezone Europe/Moscow
```

## Проверить установку

```bash
timedatectl
```

# Django

```bash
python -m pip install Django
```

```bash
django-admin --version
```

Creating a project

```bash
django-admin startproject <name>
```

The development server

```bash
python manage.py runserver
```

operations: 0 installs, 24 updates, 0 removals

- Updating idna (3.7 -> 3.10)
- Updating anyio (4.4.0 -> 4.6.0)
- Updating cffi (1.17.0 -> 1.17.1)
- Updating greenlet (3.0.3 -> 3.1.1)
- Updating multidict (6.0.5 -> 6.1.0)
- Updating pydantic-core (2.20.1 -> 2.23.4)
- Updating aiohappyeyeballs (2.3.7 -> 2.4.0)
- Updating certifi (2024.7.4 -> 2024.8.30)
- Updating cryptography (43.0.0 -> 43.0.1)
- Updating numpy (2.1.0 -> 2.1.1)
- Updating platformdirs (4.2.2 -> 4.3.6)
- Updating pydantic (2.8.2 -> 2.9.2)
- Updating pytz (2024.1 -> 2024.2)
- Updating sqlalchemy (2.0.32 -> 2.0.35)
- Updating starlette (0.38.2 -> 0.38.6)
- Updating tzdata (2024.1 -> 2024.2)
- Updating urllib3 (2.2.2 -> 2.2.3)
- Updating yarl (1.9.4 -> 1.12.1)
- Updating aiohttp (3.10.4 -> 3.10.6)
- Updating alembic (1.13.2 -> 1.13.3)
- Updating fastapi (0.112.1 -> 0.112.4)
- Updating pandas (2.2.2 -> 2.2.3)
- Updating polars (1.5.0 -> 1.8.2)
- Updating pydantic-settings (2.4.0 -> 2.5.2)

# Celery

Запуск мониторинга задач

http://127.0.0.1:5001/
```bash
celery -A tasks flower --port=5001
```

Запуск воркера

```python
import eventlet

eventlet.monkey_patch()
# остальные импорты
```

```bash
celery -A tasks worker -c 4 -n trendy --loglevel=INFO -P eventlet -Ofair
```

```python
from gevent import monkey

monkey.patch_all()
# остальные импорты
```


```bash
celery -A tasks worker -c 4 -n trendy --loglevel=INFO -P gevent
```

Запуск beat (выполнение задач по времени)

```bash
 celery -A tasks beat --loglevel=INFO
```


## 👨‍💻 Базовые команды Git

Создание репозитория:
- git init [project_name] — создать новый локальный репозиторий.
- git clone [url] — создание копии (удаленного) репозитория.

Изменения:
- git add [file] — индексировать файл, готовый к коммиту.
- git add . — индексировать все файлы, готовые к коммиту.
- git commit -m "commit message" — зафиксировать индексированные файлы с комментарием. (https://t.me/python2day)
- git commit -am "commit message" — зафиксировать все отслеживаемые файлы с комментарием.
- git reset [file] — откат изменений до определенного коммита.
- git reset --hard — вернуть дерево проекта и индекс в состояние, соответствующее указанному коммиту, удалив изменения последующих коммитов.

Отслеживание репозитория:
- git status — список новых или измененных файлов, которые еще не закоммитены.
- git diff — показать изменения, не внесенные в индекс.
- git diff --cached — изменения, внесенные в индекс. (https://t.me/python2day)
- git diff HEAD — показать все индексированные и неиндексированные изменения файлов.
- git diff commit1 commit2 — показать различия между двумя коммитами.
- git blame [file] — показать дату изменения и автора для данного файла.
- git show [commit]:[file] - показать изменения для определенного коммита или файла. (https://t.me/python2day)
- git log — показать полную историю изменений.
- git log -p [file/directory] — показать историю изменений для файла/папки, включая различия (diffs).

Работа с ветками:
- git branch — показать все локальные ветки.
- git branch -av — показать все локальные и удаленные ветки.
- git checkout my_branch — переключиться на ветку my_branch. (https://t.me/python2day)
- git branch new_branch — создание новой ветки new_branch.
- git branch -d my_branch — удалить ветку my_branch. (https://t.me/python2day)
- git checkout branch_b / git merge branch_a — объединить branch_b и branch_a.
- git tag my_tag — добавить тег к текущему коммиту.
- git tag -a my_tag -m "commit" — создать тег с комментарием.

Синхронизация:
- git fetch — получить последние изменения с удаленного сервера без слияния.
- git pull — получить последние изменения с удаленного сервера и выполнить слияние. (https://t.me/python2day)
- git pull --rebase — получить последние изменения с удаленного сервера и перебазировать.
- git push — применить локальные изменения на удаленный сервер.
- git help — показать справочную информацию о Git. (https://t.me/python2day)

.gitignore — объясняем Git, какие файлы следует игнорировать.

# 🚀 Запуск приложения

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```