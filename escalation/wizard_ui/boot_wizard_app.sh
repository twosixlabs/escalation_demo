#!/bin/sh
export FLASK_ENV=development
exec gunicorn -b 0.0.0.0:8001 --access-logfile - --error-logfile - --log-level debug --timeout 1200 --workers 1 wizard_app:app

