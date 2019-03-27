#!/bin/bash
sleep 5
export CPU_NUM=$(cat /proc/cpuinfo |grep processor|wc -l)
python manage.py collectstatic -v0 --noinput
python manage.py migrate --noinput
/usr/local/bin/gunicorn -w $((2*$CPU_NUM+1)) -b unix:/deploy/running/handle/django-tutorial-server.sock mysite.wsgi:application --log-level info
