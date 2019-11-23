PYTHON_EXECUTABLE ?= /usr/bin/python3
REQUIREMENTS_FILE ?= requirements.txt

# Setup virtualenv if not already existing
bin/python:
	virtualenv -p $(PYTHON_EXECUTABLE) .
	bin/pip install -r $(REQUIREMENTS_FILE)

migrate: bin/python
	bin/python fotogalleri/manage.py migrate

migrations: bin/python
	bin/python fotogalleri/manage.py makemigrations

deploy: bin/python
	bin/python fotogalleri/manage.py collectstatic -v0 --noinput
	touch fotogalleri/fotogalleri/wsgi.py

# Development specific
serve: bin/python
	bin/python fotogalleri/manage.py runserver 8888

shell: bin/python
	bin/python fotogalleri/manage.py shell

test: bin/python
	bin/python fotogalleri/manage.py test fotogalleri

test-pep8: bin/python
	bin/python fotogalleri/manage.py test test_pep8

test-all: bin/python
	$(MAKE) test
	$(MAKE) test-pep8

clean:
	rm -rf build/ dist/ *.egg-info/ local/

clean-all:
	$(MAKE) clean
	rm -rf bin lib include
