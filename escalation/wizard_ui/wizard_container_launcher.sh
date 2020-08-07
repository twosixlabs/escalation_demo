#!/usr/bin/env bash
# todo: assert that this is run from the top level of the repo
docker-compose run --entrypoint /escalation/wizard_ui/boot_wizard_app.sh -p "8001:8001"  -v "$(pwd)/escalation/app_deploy_data":/escalation/app_deploy_data web
