FROM python:3.7.8-buster

#Set flask_app as working directory
WORKDIR /escalation


#install dependencies
#copy data from current dir into flask_app
COPY escalation/requirements-app.txt /escalation
RUN pip install --trusted-host pypi.python.org -r requirements-app.txt

#copy data from current dir into flask_app
COPY escalation /escalation
RUN chmod +x  /escalation/boot.sh

#Use this port
EXPOSE 5000

#run app.py with python
ENTRYPOINT ["/escalation/boot.sh"]
