# Setup virtualenv if not already existing
bin/python:
	virtualenv -p /usr/bin/python .
	bin/pip install -r requirements.txt

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

clean:
	rm -rf build/ dist/ *.egg-info/ local/

clean-all:
	$(MAKE) clean
	rm -rf bin lib include
