MANAGE = python manage.py
SOURCE = src
MAIN = kinoCMS

PROJECT_DIR=$(shell pwd)
WSGI_PORT=8000
                                  
run:
	$(MANAGE) runserver 127.0.0.1:8000

gunicorn-run:
	gunicorn kinoCMS.wsgi:application -b 0.0.0.0:8000 --reload

migrations:
	$(MANAGE) makemigrations --no-input
	$(MANAGE) migrate --no-input
	$(MANAGE) collectstatic --no-input
	python fill_table.py
	gunicorn kinoCMS.wsgi:application -b 0.0.0.0:8000 --reload

gen-users:
	$(MANAGE) gen_users

gen-s:
	$(MANAGE) gen_seances

kill-port:
	sudo fuser -k 8000/tcp

diagram:
	$(MANAGE) graph_models -a -g -o my_project_visualized.png

start-app:
	cd $(SOURCE) && python manage.py startapp $(app)

migrate:
	$(MANAGE) makemigrations
	$(MANAGE) migrate

shell: # only after 'make extensions-install'
	$(MANAGE) shell_plus --print-sql

freeze:
	pip freeze > requirements.txt


worker:
	cd $(PROJECT_DIR) && celery -A $(MAIN) worker --autoscale=4,2 -l info

beat:
	cd $(SOURCE)/&& celery -A $(MAIN) beat -l info

worker-info:
	cd $(SOURCE) && celery -A $(MAIN) events


super:
	$(MANAGE) createsuperuser

install:
	pip install -r requirements.txt

check:
	$(MANAGE) check

migrations-dry:
	$(MANAGE) makemigrations --dry-run

gen-book-category:
	$(MANAGE) gen_book_category


flake8-install:
	pip install flake8
	pip install flake8-import-order # сортировку импортов
	pip install flake8-docstrings # доки есть и правильно оформлены
	pip install flake8-builtins # что в коде проекта нет переменных с именем из списка встроенных имён
	pip install flake8-quotes # проверять кавычки

	# ставим гит-хук
	flake8 --install-hook git
	git config --bool flake8.strict true

debugger-install:
	pip install django-debug-toolbar
	# 'debug_toolbar'                                    | add to the INSTALLED_APPS in settings.py
	# debug_toolbar.middleware.DebugToolbarMiddleware    | add to the MIDDLEWARE in settings.py
	# INTERNAL_IPS = [ "127.0.0.1", ]					 | create in the settings.py
	# path('__debug__/', include(debug_toolbar.urls))    | add to the urls.py in project DIR
	# import debug_toolbar                               | add to the urls.py in project DIR

extensions-install:
	pip install django-extensions
	pip install ipython
	# 'django_extensions'                                | add to the INSTALLED_APPS in settings.py

celery-install:
	pip install -U Celery
	pip install flower
