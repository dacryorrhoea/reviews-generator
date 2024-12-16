from os import getenv
import psycopg2
from dotenv import load_dotenv

load_dotenv(dotenv_path='/home/alice/ShitCode/gemini_generating_reviews/.env')


class DatabaseHandler:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                dbname=getenv('DB_NAME'),
                user=getenv('DB_USER'),
                password=getenv('DB_PASSWORD'),
                host=getenv('DB_HOST'),
                port=getenv('DB_PORT')
            )
            self.conn.autocommit = True
            self.cur = self.conn.cursor()
        except Exception as e:
            print(f'Database connect error: {e}')

    def operation_create_table(self):
        pass

    def execute(self, sql_code):
        try:
            self.cur.execute(sql_code)
            return self.cur.fetchall()
        except Exception as error:
            print(f'Error in code<<<\n{sql_code}\n>>>\nError text: {error}')
            return None

    def close_connect(self):
        self.cur.close()
        self.conn.close()
