# Copyright [2020] [Two Six Labs, LLC]

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


FROM python:3.7.8-buster

#Set flask_app as working directory
WORKDIR /escalation
ENV PYTHONPATH /escalation

#install dependencies
#copy data from current dir into flask_app
COPY escalation/requirements-app.txt /escalation
RUN pip install --trusted-host pypi.python.org -r requirements-app.txt

#copy data from current dir into flask_app
COPY escalation /escalation
RUN chmod +x /escalation/boot.sh
#
##Use this port
EXPOSE 8000

##run app.py with python
ENTRYPOINT ["/escalation/boot.sh"]
