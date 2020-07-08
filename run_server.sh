# link connects the container (named escalation-os-psql) for the sql db to the app using the alias dbserver
# escos-server is the name of the image built by escos/Dockerfile, escos-app is the name of the running app container

#docker run --name escos-app -it --rm \
#    -e DATABASE_URL=postgresql+pg8000://escalation_os:escalation_os_pwd@dbserver/escalation_os --link escalation-os-psql:dbserver \
#    -p 5000:5000 \
#    escos-server:latest


docker run --name escos-app -it --rm \
    -e DATABASE_URL=mysql+mysqlconnector://escalation_os_user:escalation_os_pwd@dbserver/escalation_os \
    --link escalation-os-mysql:dbserver \
    -p 5000:5000 \
    escos-server:latest
