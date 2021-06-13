import DB
import mysql.connector
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

db = mysql.connector.connect(
  host=config['db']['db_host'],
  user=config['db']['db_username'],
  password=config['db']['db_password']
)

cursor = db.cursor()
cursor.execute("CREATE DATABASE usmtp")

cursor.close()
db.close()


db = DB.DB()

sql = open("database/usmtp.sql", "r")
#create tables
db.execMultiple( sql.read() )

print("List of inserted tables: ")
db.exec("SHOW TABLES")

for x in db.result:
    print( x[0] )


