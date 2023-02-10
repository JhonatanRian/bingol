FROM python:3.10.0-alpine
LABEL maintainer "bingol_aplication <bingol@gmail.com>"
COPY . /var/www
WORKDIR /var/www
RUN apk update && apk add build-base bind-tools zlib-dev jpeg-dev gcc musl-dev python3-dev postgresql-dev && pip install -r requirements.txt && sh build_cython.sh
WORKDIR /var/www/bingool/bingo
RUN python3.10 setup.py build_ext --inplace
WORKDIR /var/www
ENTRYPOINT [ "python" ]
CMD [ "manage.py", "bingolapp" ]