FROM python:3.10.0-alpine
LABEL maintainer "bingol <bingol@gmail.com>"
COPY . /var/www
WORKDIR /var/www
RUN apk update && apk add zlib-dev jpeg-dev gcc musl-dev python3-dev postgresql-dev && pip install -r requirements.txt && python manage.py collectstatic --noinput
WORKDIR /var/www/bingool/bingo
RUN python3.10 setup.py build_ext --inplace
WORKDIR /var/www
ENTRYPOINT gunicorn --bind 0.0.0.0:8000 bingoool.wsgi
EXPOSE 8000
