**$OS_RELEASE** = Linux Ubuntu 16.04.3 LTS (Xenial) x64

----

##### **Install libraries, frameworks**
```
sudo chmod 777 install initdb resetdb &&\
./install
```

##### **Create database**
```
echo "
CREATE DATABASE `itline` CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER DATABASE `itline` CHARACTER SET utf8 COLLATE utf8_bin;
GRANT ALL ON `itline`.* TO 'root'@'localhost';
" | mysql -h localhost -P 3306 -u root -p
```

##### **Configure database**
```
./initdb
```

##### **Migrate database**
```
python3.6 manage.py makemigrations account &&\
python3.6 manage.py migrate --database=default
```

##### **Drop all tables**
```
./resetdb
```

##### **Test the application**
```
python3.6 manage.py test --keepdb

##### **Run HTTP server**
```
python3.6 manage.py runserver
```
