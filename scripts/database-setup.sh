#!/bin/sh
sudo docker exec -ti admin-mysql_db.1.0wgtxijosd6k0no4gmlskxlmw mysql -pstudent -u "root" -Bse "CREATE DATABASE IF NOT EXISTS BE_171884; CREATE USER IF NOT EXISTS 'BE_171884'@'%' IDENTIFIED BY 'jajahagrida'; GRANT ALL PRIVILEGES ON BE_171884.* TO 'BE_171884'@'%' WITH GRANT OPTION;"
sudo docker exec -i admin-mysql_db.1.0wgtxijosd6k0no4gmlskxlmw mysql -p"jajahagrida" -u "BE_171884" BE_171884 < ./backup.sql
