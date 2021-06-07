import mysql.connector as connector
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

class DB:
    def __init__(self):
        self.db = connector.connect(
            host=config['db']['db_host'],
            user=config['db']['db_username'],
            password=config['db']['db_password'],
            database="usmtp",
            port=3306
        )
    def exec(self, query, values=(), multiple=False):
        executor = self.db.cursor() 
        executor.execute(query, values, multi=multiple)
        self.result = executor

    def execMultiple(self, query):
        executor = self.db.cursor() 
        for x in executor.execute(query, multi=True):
            pass
        executor.close()

    def __del__(self):
        self.db.close()




