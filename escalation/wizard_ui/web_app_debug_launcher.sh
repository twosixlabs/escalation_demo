#!/usr/bin/env bash
# launch the web app using a debug mode,
# mounting the app_deploy data directly in order to monitor and relaunch when changed by the config wizard
docker-compose run --entrypoint /escalation/wizard_ui/boot_escalation_debug_mode.sh \
-p "8000:8000" \
-v "$(pwd)/escalation/app_deploy_data":/escalation/app_deploy_data \
web