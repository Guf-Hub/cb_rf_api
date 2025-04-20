.PHONY: build up down list logs clean pure

# Сборка Docker-образов без использования кэша
build:
	docker compose build --no-cache

# Запуск всех сервисов, определенных в docker-compose.yaml, с пересборкой
rebuild:
	docker compose down --volumes --remove-orphans
	docker system prune -a --volumes -f
	sudo apt-get autoremove -y
	sudo apt-get clean
	docker compose -f docker-compose.yaml up --build -d

up:
	docker compose -f docker-compose.yaml up -d

# Остановка всех запущенных сервисов и удаление осиротевших контейнеров
down:
	docker compose -f docker-compose.yaml down --remove-orphans

stop:
	docker compose -f docker-compose.yaml stop

restart:
	docker compose -f docker-compose.yaml restart

# Список всех контейнеров, включая остановленные
list:
	docker compose ps -a

# Список всех образов
images:
	docker compose images

# Команда для входа в контейнер
in_app:
	docker compose exec app bash

# Команда для просмотра логов
logs:
	@docker compose logs -f $(name)

# Остановка и удаление всех контейнеров и связанных с ними томов
# Удаление временных и кэшированных данных
clean:
	docker compose down -v
	rm -rf data/*
	rm -rf cookies/*
	rm -rf __pycache__
	rm -rf .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} +

# Полная очистка Docker-системы
pure:
	docker compose down --volumes --remove-orphans
	docker system prune -a --volumes -f
	# Остановка всех запущенных контейнеров, если они есть
	#	@if [ -n "$$(docker ps -q)" ]; then docker stop $$(docker ps -q); fi
	#	# Удаление всех контейнеров
	#	@if [ -n "$$(docker ps -aq)" ]; then docker rm $$(docker ps -aq); fi
	#	# Удаление всех неиспользуемых образов, контейнеров, томов и сетей
	#	docker system prune -a --volumes -f
	#	# Удаление всех неиспользуемых данных сборки
	#	docker builder prune -f
	#	# Удаление всех неиспользуемых томов
	#	docker volume prune -f
	#	# Удаление всех неиспоьзуемых сетей
	#	docker network prune -f

docker-update:
	docker-update:
	sudo apt-get update
	sudo apt-get install docker-ce docker-ce-cli containerd.io
	sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
	sudo chmod +x /usr/local/bin/docker-compose
	docker --version
