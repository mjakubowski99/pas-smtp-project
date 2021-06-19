# pas-smtp-project
Mail server created according to own SMTP protocol creation

Authors:  
Mateusz Kopczan, Michał Jakubowski


Install required python packages:  
```
pip install cryptography
python -m pip install mysql-connector-python
```  
To init database run some mysql database server and specify data in config.ini file.   
We use mysql local database server provided by Laragon environment. You can choose what you want.  
Default settings for config.ini are shown below.     
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
This will create database called usmtp and seed data with example users.


Last step is running: (Remember to have running mysql database because script after running try to connect to db)

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
In this script you have 3 posibilities which you can choose with input commands shown below:   
    1.You can create your self signed certificate with:   
      ```
        CREATE_CERT_REQ
      ```  
    2.You can gen certificate request with:  
      ```
        GEN_ROOT_CERT
      ```  
    3.You can sign certificate request with:  
      ```
        SIGN_CERT
      ```  
After choosing options you must follow program instructions and provide required data.  
Remember to provide filenames which not exists, because script protect files from overwriting.  

You can find root certificate files in this directory --> ssl/rootCert  
Signed certificate files can be founded there --> ssl/certs  
Private rsa keys can be found here --> ssl/keys  
Public rsa keys can be found here --> ssl/clientKeys  

Some more comments to implementation are describied in documentation






