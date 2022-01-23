FROM python:3.9.10-slim-buster

WORKDIR /app

RUN pip3 install django
RUN pip3 install channels
RUN pip3 install channels-redis

COPY . .

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8008"]
