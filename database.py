from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
SQLALCHEMY_MYSQL_URL = "mysql+mysqldb://root:abattoir94@localhost/project_management"

engine = create_engine(SQLALCHEMY_MYSQL_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()