up:
	docker compose up --build -d

flake:
	docker compose run --rm app sh -c "flake8"

build:
	docker compose build

down:
	docker compose down

test:
	docker compose run --rm app sh -c "python manage.py test"

clean: down
	docker compose down --rmi all

fclean: clean
	docker volume ls -q | grep dev-db-data | xargs --no-run-if-empty docker volume rm

ls:
	docker compose images
	docker compose ps
	docker volume ls
