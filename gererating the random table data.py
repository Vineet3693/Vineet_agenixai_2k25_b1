import psycopg2
from faker import Faker
import random


fake = Faker()


DB_NAME = "lms_db"
DB_USER = "postgres"          
DB_PASSWORD = "233223" 
DB_HOST = "localhost"         
DB_PORT = "5432"              

try:
    
    connection = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = connection.cursor()
    print("Connected to the database successfully!")

    
    print("Inserting data into 'authors' table...")
    for _ in range(100):
        name = fake.name()
        birth_year = random.randint(1900, 2000)
        cursor.execute(
            "INSERT INTO authors (name, birth_year) VALUES (%s, %s);",
            (name, birth_year)
        )

    
    print("Inserting data into 'books' table...")
    genres = ['Fantasy', 'Science Fiction', 'Mystery', 'Non-Fiction', 'Romance']
    for _ in range(25):
        title = fake.sentence(nb_words=3).replace("'", "''")
        genre = random.choice(genres)
        publication_year = random.randint(1990, 2025)
        cursor.execute(
            "INSERT INTO books (title, genre, publication_year) VALUES (%s, %s, %s);",
            (title, genre, publication_year)
        )

    
    print("Inserting data into 'customers' table...")
    for _ in range(10):
        name = fake.name()[:10]  # Truncate to 15 characters
        email = fake.email()
        phone = fake.msisdn()[:10]  # Ensure phone numbers fit
        cursor.execute(
            "INSERT INTO customers (name, email, phone) VALUES (%s, %s, %s);",
            (name, email, phone)
        )


    
    print("Inserting data into 'transactions' table...")
    for _ in range(50):
        book_id = random.randint(1, 50)  # Assuming 50 books exist
        customer_id = random.randint(1, 15)  # Assuming 15 customers exist
        issue_date = fake.date_between(start_date='-1y', end_date='today')
        return_date = issue_date if random.random() > 0.5 else None
        cursor.execute(
            "INSERT INTO transactions (book_id, customer_id, issue_date, return_date) VALUES (%s, %s, %s, %s);",
            (book_id, customer_id, issue_date, return_date)
        )

    
    connection.commit()
    print("Data inserted successfully!")

except Exception as error:
    print("Error occurred:", error)

finally:
    
    if connection:
        cursor.close()
        connection.close()
        print("Database connection closed.")
