FROM postgres:13.1-alpine
LABEL maintainer "bingol <bingol@gmail.com>"
ENV POSTGRES_USER=bingol_user
ENV POSTGRES_PASSWORD=Bingol2023
ENV POSTGRES_DB=bingol_db
EXPOSE 5432
