FROM debian:12-slim

ARG MYSQL_HOST_ARG=undefined
ENV MYSQL_HOST=${MYSQL_HOST_ARG}

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      python3 \
      python3-pymysql \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /srv/myapp
COPY client.py .

EXPOSE 8000
CMD ["python3", "client.py"]
