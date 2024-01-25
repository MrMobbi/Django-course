up:
	docker compose up --build -d

flake:
	docker compose run --rm app sh -c "flake8"

build:
	docker compose build

down:
	docker compose down

clean:
	docker compose down --rmi all

ls:
	docker compose images
	docker compose ps
	docker volume ls
