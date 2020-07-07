from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from flask_sqlalchemy import SQLAlchemy

from app_settings import PSQL_DATABASE_CONFIG as database_config

try:
    from database.models import *
    from database.models import Base
except ModuleNotFoundError:
    raise (ModuleNotFoundError, "models.py file not defined- run database setup")


db = SQLAlchemy()
engine = create_engine(URL(**database_config), convert_unicode=True)
Base.metadata.create_all(bind=engine)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

# allows us to use the table_class.query instead of db.session.query(table_class)
Base.query = db_session.query_property()
