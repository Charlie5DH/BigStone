## Automação Cantina

#### controleCantina.py
 * leitura do peso da balança via porta serial
 * leitura de código de barras com o ID do cliente via porta USB

#### Pacotes necessarios
```

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

```



