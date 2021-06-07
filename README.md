# pas-smtp-project
Mail server created according to own SMTP protocol creation


Install required python packages:  
```
pip install cryptography
python -m pip install mysql-connector-python
```  
To init database run some database server and specify data in config.ini file.
Default settings are shown below  
```
[db]
db_host = localhost
db_username = root
db_password = 
```

Next run:  
```
py database/InitDB.py
```
This will create database called usmtp 
