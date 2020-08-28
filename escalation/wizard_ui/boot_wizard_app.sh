#!/bin/sh
export FLASK_ENV=development
export FLASK_APP=app.py
export DEBUG=true
export FLASK_RUN_EXTRA_FILES="/escalation/app_deploy_data/"
flask run --host=0.0.0.0 --port=8001 --extra-files $FLASK_RUN_EXTRA_FILES