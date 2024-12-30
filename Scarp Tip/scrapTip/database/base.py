from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


Base = declarative_base()


class DatabaseManager:
    _instance = None


    def __new__(cls, connection_string=None):
        if not cls._instance:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.connection_string = connection_string
            cls._instance.engine = None
            cls._instance.Session = None
        return cls._instance


    def initialize(self, connection_string):
        self.connection_string = connection_string
        self.engine = create_engine(connection_string, pool_pre_ping=True)
        self.Session = sessionmaker(bind=self.engine)


    def create_tables(self):
        Base.metadata.create_all(self.engine)


    def get_session(self):
        if not self.Session:
            raise ValueError("Error Found Connecting Database - 404")
        return self.Session()