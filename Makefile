migrate:
	python ./backend/manage.py makemigrations
	python ./backend/manage.py migrate
b-run:
	python ./backend/manage.py runserver
check:
	python ./backend/manage.py check
