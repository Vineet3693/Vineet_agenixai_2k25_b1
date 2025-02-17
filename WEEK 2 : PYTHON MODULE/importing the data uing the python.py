import psycopg2

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    dbname="api_databse", 
    user="catapi", 
    password="233223", 
    host="localhost", 
    port="5432"
)

# Create a cursor object
cur = conn.cursor()

# Execute a query
cur.execute("SELECT * FROM table")

# Fetch results
rows = cur.fetchall()

# Do something with the results
for row in rows:
    print(row)

# Close cursor and connection
cur.close()
conn.close()
