from db import engine, Base
from models import *
from sqlalchemy.schema import CreateTable
from sqlalchemy.dialects import postgresql

def create_schema():
    Base.metadata.create_all(engine)
    print("✅ Schema created in PostgreSQL")

def print_ddl():
    for table in Base.metadata.sorted_tables:
        ddl = str(CreateTable(table).compile(dialect=postgresql.dialect()))
        print(ddl + ";\n")

if __name__ == '__main__':
    create_schema()
    print_ddl()  # Optional
