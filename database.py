from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"

DATABASE_URI = "postgresql://postgres:Michal1234@localhost/to_do"

engine = create_engine(DATABASE_URI,echo=True)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)
