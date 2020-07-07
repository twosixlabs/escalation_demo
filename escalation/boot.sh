#!/bin/sh
source venv/bin/activate
#flask db upgrade
exec gunicorn -b 0.0.0.0:5000 --access-logfile - --error-logfile - --log-level debug --timeout 1200 --workers 2 app:app

