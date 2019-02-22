FROM postgres:11-alpine
ADD init.sh /docker-entrypoint-initdb.d/
ENV POSTGRES_USER postgres
ENV DJ_DB_USER docker
ENV DJ_DB_PASSWORD docker
ENV DJ_DB_DATABASE django_tutorial
