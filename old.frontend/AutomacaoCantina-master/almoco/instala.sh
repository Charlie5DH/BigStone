#!/bin/bash

echo "Instalando dependencia do Controlador Cantina"
echo "Local: " `pwd`

echo "Instalando servico"
if test -f ./service/controle_cantina.service ; then
   sudo cp -p ./service/controle_*.service /lib/systemd/system/
   sudo systemctl enable controle_cantina
   sudo systemctl enable controle_barcode
fi

exit

sudo apt-get install git
git clone git@gitlab.com:Cantina/AutomacaoCantina.git

sudo apt-get install python-serial python-twisted
sudo apt-get install python-tornado
sudo apt-get install python-mysqldb
sudo apt-get install python-requests
sudo apt-get install python-netifaces
sudo apt-get install apache2

sudo apt-get install mysql-server
sudo mysql_secure_installation
sudo apt-get install phpmyadmin 

sudo mysql -u root -p
Enter password: 
> GRANT ALL PRIVILEGES ON mydb.* TO 'root'@'localhost' IDENTIFIED BY 'dariva12';

sudo timedatectl set-timezone America/Sao_Paulo

