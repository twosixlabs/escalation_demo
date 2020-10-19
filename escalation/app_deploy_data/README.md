This directory contains configuration jsons and a models.py file that define the app.

`main_config.json` Defines the layout of the Escalation dashboard

Each other panel of the dashboard gets its own configuration json.

`models.py` is generated automatically using the sqlalchemy code generator library `sqlacodegen`, and defines in Python the tables that exist in the linked database.


# Deploy to Portainer 

# Moving local db to portainer:

1.Dump local db to file

    docker exec -i escos_db pg_dump --username escalation escalation > penguin_pg_dump.sql
    
2. scp dump to tacc

3. on portainer db container, run:


    apt update
    apt install -y openssh-client
    scp nleiby@login1.maverick2.tacc.utexas.edu:/work/05839/nleiby/maverick2/penguin_pg_dump.sql .
    psql -U escalation -d escalation -f penguin_pg_dump.sql 