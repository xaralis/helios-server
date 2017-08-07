FROM debian:latest

EXPOSE 80

RUN apt-get update

RUN apt-get install -y python-software-properties software-properties-common

RUN apt-get upgrade -y && apt-get -y install python-virtualenv python-pip postgresql postgresql-client unzip libpq-dev postgresql-server-dev-all python-dev rabbitmq-server

ADD https://github.com/pirati-cz/helios-server/archive/master.zip /helios/

WORKDIR /helios/

RUN unzip master.zip

WORKDIR /helios/helios-server-master/

RUN virtualenv venv

RUN bash -c 'source venv/bin/activate; pip install -r requirements.txt'

RUN echo 'local   all             all                                     trust' > /etc/postgresql/9.4/main/pg_hba.conf

VOLUME /var/lib/postgresql

ADD docker-entrypoint.sh /

ENTRYPOINT /docker-entrypoint.sh

