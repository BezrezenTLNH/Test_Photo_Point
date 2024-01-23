install:
	poetry install

start:
	poetry run python manage.py runserver

lint:
	poetry run flake8 task_manager

migrate:
	poetry run python manage.py makemigrations && poetry run python manage.py migrate
