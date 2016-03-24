#!/bin/bash

trap "echo TRAPed signal" HUP INT QUIT KILL TERM

chown postgres:postgres /var/lib/postgresql

/etc/init.d/postgresql start

echo 'CREATE USER root;' | psql -U postgres
echo 'CREATE DATABASE helios;' | psql -U postgres 2>&1 | grep -q "already exists"
HASDB=$?

source venv/bin/activate

if [ \! ${HASDB} ]; then
	python manage.py syncdb
fi

python manage.py migrate

python manage.py runserver 0.0.0.0:80

/etc/init.d/postgresql stop

