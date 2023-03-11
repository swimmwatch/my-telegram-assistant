"""
Sync database client.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from services.db.config import DatabaseSettings

database_settings = DatabaseSettings()
engine = create_engine(database_settings.db_url, echo=database_settings.debug)
Session_ = scoped_session(sessionmaker(bind=engine))
