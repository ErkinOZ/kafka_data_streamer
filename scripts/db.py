
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://dev:dev123@localhost:5432/demo"
engine = create_engine(DATABASE_URL)
