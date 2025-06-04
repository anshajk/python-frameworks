import os

# from psycopg import ConnectionPool
from psycopg_pool import pool
from dotenv import load_dotenv


load_dotenv()

connection_string = os.getenv("POSTGRES_CONN_URL")
# Create a connection pool
connection_pool = pool.ConnectionPool(
    min_size=1,  # Minimum number of connections in the pool
    max_size=5,  # Maximum number of connections in the pool
    conninfo=connection_string,
)
# Check if the pool was created successfully
if connection_pool:
    print("Connection pool created successfully")
# Get a connection from the pool
conn = connection_pool.getconn()
# Create a cursor object
cur = conn.cursor()
# Execute SQL commands to retrieve the current time and version from PostgreSQL
cur.execute("SELECT * FROM employees.employee limit 10;")
rows = cur.fetchall()
for row in rows:
    print(row)


cur.close()

connection_pool.putconn(conn)
# Close all connections in the pool
connection_pool.close()
