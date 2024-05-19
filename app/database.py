import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

# SQLALCHEMY_DATABASE_URL = 'sqlite:///blog.db'
# SQLALCHEMY_DATABASE_URL = "postgresql://blogger:FzWbeUEVYqux9n4sNBqxl8EcEBhh97gC@dpg-cofvha7sc6pc7382ua90-a.oregon-postgres.render.com/blogdb_brle"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"
# SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:postgrepass@localhost:5432/fastapidb"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind = engine, autocommit = False, autoflush = False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    
    try:
        yield db
        
    finally:
        db.close()



# try:
#   # Connect to the PostgreSQL database
#   conn = psycopg2.connect(host=settings.database_hostname, database=settings.database_name, user=settings.database_username, password=settings.database_password)

#   # Create a cursor object
#   cur = conn.cursor()

#   # Sample PostgreSQL code (replace with your actual query)
#   sql = "SELECT * FROM your_table;"

#   # Execute the query
#   cur.execute(sql)

#   # Fetch results (if applicable)
#   rows = cur.fetchall()
  
#   # Print results (if applicable)
#   for row in rows:
#     print(row)

#   # Commit changes (if applicable)
#   # conn.commit()

# except (Exception, psycopg2.Error) as error:
#   print("Error while connecting to PostgreSQL", error)
# finally:
#   # Close the cursor and connection
#   if cur is not None:
#     cur.close()
#   if conn is not None:
#     conn.close()