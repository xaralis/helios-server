#!/bin/bash

trap "echo TRAPed signal" HUP INT QUIT KILL TERM

source venv/bin/activate

/etc/init.d/postgresql start

if [ -f /.firstrun ]; then
	echo 'CREATE USER root; CREATE DATABASE helios;' | psql -U postgres
	./reset.sh
	rm /.firstrun
fi

python manage.py runserver 0.0.0.0:80

/etc/init.d/postgresql stop

