import DB
import mysql.connector
import configparser
import hashlib

config = configparser.ConfigParser()
config.read('config.ini')

db = mysql.connector.connect(
  host=config['db']['db_host'],
  user=config['db']['db_username'],
  password=config['db']['db_password']
)

cursor = db.cursor()
cursor.execute("CREATE DATABASE usmtp")




db = DB.DB()

sql = open("database/usmtp.sql", "r")
#create tables
db.execMultiple( sql.read() )

print("List of inserted tables: ")
db.exec("SHOW TABLES")

for x in db.result:
    print( x[0] )


sha = hashlib.sha256()
sha.update("example123".encode())
password = sha.hexdigest()

db.insert("""INSERT INTO users (id, name, email, email_verified_at, password, remember_token, created_at, updated_at) VALUES
                    (0, "Test1", "testprotokolu1@wp.pl", null, %s, null, null, null)""", (password,))
db.insert("""INSERT INTO users (id, name, email, email_verified_at, password, remember_token, created_at, updated_at) VALUES
                    (1, "Test1", "testprotokolu2@wp.pl", null, %s, null, null, null)""", (password,))
db.insert("""INSERT INTO users (id, name, email, email_verified_at, password, remember_token, created_at, updated_at) VALUES
                    (2, "Test1", "testprotokolu3@wp.pl", null, %s, null, null, null)""", (password,))
db.insert("""INSERT INTO users (id, name, email, email_verified_at, password, remember_token, created_at, updated_at) VALUES
                    (3, "Test1", "testprotokolu4@wp.pl", null, %s, null, null, null)""", (password,))
db.insert("""INSERT INTO users (id, name, email, email_verified_at, password, remember_token, created_at, updated_at) VALUES
                    (4, "Test1", "testprotokolu5@wp.pl", null, %s, null, null, null)""", (password,))
db.insert("""INSERT INTO users (id, name, email, email_verified_at, password, remember_token, created_at, updated_at) VALUES
                    (5, "Test1", "testprotokolu6@wp.pl", null, %s, null, null, null)""", (password,))

print("List of users for testing: (password for all users: example123)")
db.exec("SELECT email FROM users")
for x in db.result:
  print(x[0])


#db.insert("Commit")
#cursor.close()
#db.close()
    






