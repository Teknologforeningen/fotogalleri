FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
RUN apt update && apt install -y git libpq-dev libsasl2-dev python-dev libldap2-dev libssl-dev
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
CMD [ "python3", "fotogalleri/manage.py", "runserver", "0.0.0.0:8888" ]
