import requests
import psycopg2
from psycopg2 import sql
import logging

# Set up logging to capture messages
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GitHubAPI:
    def __init__(self, username, api_url="https://api.thecatapi.com/v1/images/search?limit=10"):
        """Constructor to initialize GitHub username and API URL."""
        self.username = username
        self.api_url = api_url.format(username)
    
    def fetch_data(self):
        """Fetch repository data from cat API from the github public api library ."""
        try:
            logger.info(f"Fetching repositories for user: {self.username}")
            response = requests.get(self.api_url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data: {e}")
            return None


class Database:
    def __init__(self, host, port, dbname, user, password):
        """Constructor to initialize the database connection parameters."""
        self.host = host
        self.port = 5432
        self.dbname = api_database 
        self.user = user
        self.password = 233223
    
    def connect(self):
        """Establish a connection to the PostgreSQL database."""
        try:
            logger.info("Connecting to the PostgreSQL database...")
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                dbname=self.dbname,
                user=self.user,
                password=self.password
            )
            return conn
        except Exception as e:
            logger.error(f"Error connecting to the database: {e}")
            return None
    
    def insert_data(self, data):
        """Insert repository data into the PostgreSQL database."""
        conn = self.connect()
        if conn is None:
            return
        
        cursor = conn.cursor()
        insert_query = """
            INSERT INTO github_repos (repo_name, repo_url, description, created_at) 
            VALUES (%s, %s, %s, %s)
        """
        
        try:
            for item in data:
                values = (item['name'], item['html_url'], item['description'], item['created_at'])
                cursor.execute(insert_query, values)
            
            # Commit the transaction
            conn.commit()
            logger.info(f"Successfully inserted {len(data)} records into the database.")
        except Exception as e:
            logger.error(f"Error inserting data into the database: {e}")
            conn.rollback()  # Rollback in case of error
        finally:
            cursor.close()
            conn.close()


class GitHubToPostgres:
    def __init__(self, username, api_database):
        """Constructor to initialize GitHub username and database parameters."""
        self.github_api = GitHubAPI(username)
        self.database = Database(api_database)

    def extract_and_load(self):
        """Fetch data from GitHub API and load it into PostgreSQL database."""
        data = self.github_api.fetch_data()
        if data:
            self.database.insert_data(data)
        else:
            logger.warning("No data fetched from GitHub API.")

