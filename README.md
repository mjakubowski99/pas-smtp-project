# pas-smtp-project
Mail server created according to own SMTP protocol creation

Authors:  
Mateusz Kopczan, Michał Jakubowski


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

Next run in project root folder:  
```
py database/InitDB.py
```
This will create database called usmtp 

Last step is running: (Remember to have running database)

```
py server.py
```
And
```
py client.py
```
To init server and client communication

# Ssl certificates managing:

You can run:
```
py certManager.py
```
In this script you have 3 posibilities.   
You can create your self signed certificate.  
You can gen certificate request and you can sign certificate request.


