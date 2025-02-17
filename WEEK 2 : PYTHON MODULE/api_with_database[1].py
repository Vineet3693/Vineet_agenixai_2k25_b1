import requests
import psycopg2
from psycopg2 import sql
import json

# Defining  the API endpoint and the parameters
API_URL = 'https://api.thecatapi.com/v1/images/search?limit=10'  # API URL
API_KEY = 'api_key'  # If authentication is required
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'api_database'
DB_USER = 'db_user'
DB_PASSWORD = '2333223'

def fetch_data_from_api():
    """Fetches data from the API."""
    headers = {'Authorization': f'Bearer {API_KEY}'}
    response = requests.get(API_URL, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # Assuming the API returns JSON data
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

def connect_to_db():
    """Establish a connection to the PostgreSQL database."""
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

def insert_data_into_db(data):
    """Inserts the API data into the PostgreSQL database."""
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        # Assuming 'data' is a list of dictionaries where each dictionary represents a row
        for item in data:
            # Adjust this SQL to match your table and column names
            insert_query = sql.SQL("""
                INSERT INTO your_table_name (column1, column2, column3) 
                VALUES (%s, %s, %s)
            """)
            values = (item['field1'], item['field2'], item['field3'])
            cursor.execute(insert_query, values)
        
        # Commit the transaction
        conn.commit()
        print(f"Successfully inserted {len(data)} records into the database.")
    
    except Exception as e:
        print(f"Error inserting data: {e}")
        conn.rollback()  # Rollback the transaction if there was an error
    
    finally:
        cursor.close()
        conn.close()