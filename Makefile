VENV=venv

install: $(VENV)/bin/python

bin/python:
	virtualenv -p /usr/bin/python .
	$(VENV)/bin/pip install -r requirements.txt

migrate: bin/python
	$(VENV)/bin/python fotogalleri/manage.py migrate

serve: bin/python
	$(VENV)/bin/python fotogalleri/manage.py runserver 8888

deploy: bin/python
	$(VENV)/bin/python fotogalleri/manage.py collectstatic -v0 --noinput
	touch fotogalleri/fotogalleri/wsgi.py

clean:
	rm -rf build/ dist/ *.egg-info/ local/ $(VENV)/
