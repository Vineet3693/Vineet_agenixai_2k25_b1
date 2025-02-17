import re
import psycopg2
import logging
from datetime import datetime

# Set up logging to capture messages
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ApacheLogParser:
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path
        # Regular expression to capture the Apache Common Log Format
        self.log_pattern = re.compile(
            r'(?P<ip_address>\S+) - - \[(?P<timestamp>.*?)\] "(?P<method>\S+) (?P<url>\S+) \S+" (?P<status_code>\d+) \S+ "(?P<referrer>.*?)" "(?P<user_agent>.*?)"'
        )
    
    def parse_log(self):
        """Parses the Apache log file and yields extracted data."""
        with open(self.log_file_path, 'r') as log_file:
            for line in log_file:
                match = self.log_pattern.match(line)
                if match:
                    log_data = match.groupdict()
                    log_data['timestamp'] = datetime.strptime(log_data['timestamp'], '%d/%b/%Y:%H:%M:%S %z')
                    log_data['os'] = self.extract_os(log_data['user_agent'])
                    yield log_data
                else:
                    logger.warning(f"Skipping invalid log line: {line}")
    
    def extract_os(self, user_agent):
        """Extract the OS from the User-Agent string."""
        if "Windows" in user_agent:
            return "Windows"
        elif "Mac" in user_agent:
            return "Mac OS"
        elif "Linux" in user_agent:
            return "Linux"
        elif "Android" in user_agent:
            return "Android"
        elif "iPhone" in user_agent:
            return "iOS"
        return "Unknown"

class Database:
    def __init__(self, host, port, dbname, user, password):
        """Constructor to initialize the database connection parameters."""
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
    
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
    
    def insert_log_data(self, logs):
        """Insert extracted log data into PostgreSQL."""
        conn = self.connect()
        if conn is None:
            return
        
        cursor = conn.cursor()
        insert_query = """
            INSERT INTO webserver_logs (ip_address, timestamp, method, url, status_code, referrer, os, user_agent) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            for log in logs:
                values = (log['ip_address'], log['timestamp'], log['method'], log['url'], 
                          log['status_code'], log['referrer'], log['os'], log['user_agent'])
                cursor.execute(insert_query, values)
            
            # Commit the transaction
            conn.commit()
            logger.info(f"Successfully inserted {len(logs)} records into the database.")
        except Exception as e:
            logger.error(f"Error inserting data into the database: {e}")
            conn.rollback()  # Rollback in case of error
        finally:
            cursor.close()
            conn.close()

class LogProcessor:
    def __init__(self, log_file_path, db_params):
        self.parser = ApacheLogParser(log_file_path)
        self.database = Database(**db_params)

    def process_logs(self):
        """Parse logs and insert them into the database."""
        logs = []
        for log in self.parser.parse_log():
            logs.append(log)
        
        if logs:
            self.database.insert_log_data(logs)
        else:
            logger.warning("No logs to insert into the database.")


