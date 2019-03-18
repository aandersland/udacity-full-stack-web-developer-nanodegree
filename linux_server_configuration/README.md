# Overview
This project is focused on taking a base installation of an Ubuntu 16.04 server and prepare it to be hosted on AWS.
    
* Install required libraries
* Secure the server from attack vectors
* Install and configure the database server
* Deploy an existing web application [Project 2 - Catalog App](https://github.com/aandersland/udacity-full-stack-web-developer-nanodegree/tree/master/catalog_app)

# Setup
## Setup Amazon Lightsail Instance
This section will setup your initial instance, configure firewall rules, and set a static ip address.
1. Log into you account and click on 'Create Instance'
2. select 'Linux/Unix'
3. Select 'OS Only' and then 'Ubuntu 16.04 LTS'
4. Select the cheapest plan
5. Set the instance name as **Catalog_App**
6. Select 'Create Instance'
7. Once your instance is created and running, click on your 'Catalog_App' instance
8. Then click on 'Networking'
9. Add the following firewall rules:
    * **Custom - UDP - 123**
    * **Custom - TCP - 2200**
10. Click on Create StaticIP
11. Change your static IP name to **Catalog_App_IP**
12. Click create

##Create system accounts
This section will create a grader account for running the application and a catalog_app user for the database.
1. Click on 'Connect'
2. Click on 'Connect using SSH'
3. In the new window run the following commands:
4. Run **sudo adduser grader**
5. Create a password
6. Enter the Full name: **grader**
7. Click enter for the remaining entries
8. Run **sudo adduser catalog_app**
9. Create a password
10. Enter the Full name: **catalog_app**
11. Click enter for the remaining entries

## Grader sudo access
This section will grant sudo access to the system accounts.
1. Run **sudo ls /etc/sudoers.d** (You should see a file called 90-cloud-init-users)
2. Run **sudo cp /etc/sudoers.d/90-cloud-init-users /etc/sudoers.d/grader**
3. Run **sudo nano /etc/sudoers.d/grader**
4. In the file replace **ubuntu** with **grader** and save
5. Run **su - grader** and then enter the password
6. Run **sudo -l**
7. You should see the following:
    * Matching Defaults entries for grader on ip-172-26-11-207.us-east-2.compute.internal:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin . . .
8. Run **sudo cp /etc/sudoers.d/grader /etc/sudoers.d/catalog_app**
9. Run **sudo nano /etc/sudoers.d/catalog_app**
10. In the file replace **grader** with **catalog_app** and save
11. Run **su - catalog_app** and then enter the password
12.Run **sudo -l**
13. You should see the following:
    * Matching Defaults entries for catalog_app on ip-172-26-11-207.us-east-2.compute.internal: 
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin . . .
14. Run **su - grader** and then enter the password

## Setup SSH keys for the Grader account
1. Download Putty Key Generator and start the application
2. Click on 'Generate' and follow the instructions to create a key
3. Enter a passphrase
4. Click on 'save private key' and name the file **grader_private**
5. Click on 'save public key' and name the file **grader_public**
6. Copy the contents from the Key section (Public key for pasting into OpenSSH authorized_keys file:)
7. Run **chmod 700 .ssh**
8. Run **sudo chmod 644 .ssh/authorized_keys**
9. Run **/etc/ssh/sshd_config**
    * Change the Port from **22** to **2200**
    * ensure that PasswordAuthentication = no
10. Run **sudo service ssh restart**

Start the Putty Configuration app
Enter the public pip address
Change the port to 2200
On the left panel click on SSH > Auth
On the right panel browse to the **grader_private** file 
On the left panel click on Session
Enter a name in the Saved Session box **grader**
Click on Save
Click on Open
Click on yes on the pop up window
Enter username / password

##Configure UFW Firewall
Run **sudo ufw default deny incoming**
Run **sudo ufw default allow outgoing**
Run **sudo ufw allow 2200/tcp**
Run **sudo ufw allow www**
Run **sudo ufw allow 123/udp**
Run **sudo ufw deny 22**
Run **sudo ufw enable**
Type in Y for the warning that comes up.
Run **sudo ufw status**
Your output should look like this:
Status: active

To                         Action      From
--                         ------      ----
2200/tcp                   ALLOW       Anywhere
80/tcp                     ALLOW       Anywhere
123/udp                    ALLOW       Anywhere
22                         DENY        Anywhere
2200/tcp (v6)              ALLOW       Anywhere (v6)
80/tcp (v6)                ALLOW       Anywhere (v6)
123/udp (v6)               ALLOW       Anywhere (v6)
22 (v6)                    DENY        Anywhere (v6)
Run **exit**

## Update Lightsail instance - disable port 22
Click on your Catalog_App instance
Click on Networking
Delete the following firewall rule:
* SSH - TCP - 22
Click Save

## Update server packages
Run **sudo apt-get update**
Run **sudo apt-get upgrade**

##Install PostgreSql
Run **sudo apt-get install postgresql postgresql-contrib**


##Configure database
Run **sudo su - postgres**
Run **psql**
Run **create role catalog_app with login password 'catalog_app';**
Run **alter role catalog_app createdb;**
Run **\q**
Run **exit**

#Setup Database
Run **su - catalog_app**
Run **createdb catalog_app**




##Install Apache
Run **sudo apt-get install apache2**
In a web browser type in your public ip address (3.16.230.142)
You should see the "Apache2 Ubuntu Default Page"

##Install WSGI
Run **sudo apt-get install libapache2-mod-wsgi python-dev**
**sudo a2enmod wsgi** ??
**sudo service apache2 start** ??
 cd /var/www/
 sudo git clone https://github.com/aandersland/udacity-full-stack-web-developer-nanodegree.git catalog_app
 sudo chown -R grader:grader catalog_app/
 cd /var/www/catalog_app/catalog_app
 mv application.py __init__.py
 nano __init__.py
 
 CLIENT_ID = json.loads(open('client_secrets.json', 'r')
                       .read())['web']['client_id']
                       
CLIENT_ID = json.loads(open('/var/www/catalog_app/catalog_app/client_secrets.json', 'r')
                       .read())['web']['client_id']
 
 change line 25 engine = create_engine('sqlite:///category.db') to 
 engine = create_engine('postgresql://catalog_app:password@localhost/catalog_app')
 change lines 460/461 from 
    app.debug = True
    app.run(host='0.0.0.0', port=5000, threaded=False)
 to 
 app.run()

 nano database_setup.py
 line 26 comment
 add  engine = create_engine('postgresql://catalog_app:password@localhost/catalog_app')

nano category_books.py
 comment line 6
 add engine = create_engine('postgresql://catalog_app:**password**@localhost/catalog_app')

python database_setup.py
python category_books.py
python __init__.py
CTRL+C
deactivate

## Enable virtual host
sudo nano /etc/apache2/mods-enabled/wsgi.conf
add WSGIPythonPath /var/www/catalog_app/catalog_app/venv/lib/python2.7/site-packages
 sudo nano /etc/apache2/sites-available/catalog_app.conf

<VirtualHost *:80>
    ServerName 3.16.230.142
    ServerAlias ec2-3.16.230.142.us-east-2a.compute.amazonaws.com
    WSGIScriptAlias / /var/www/catalog_app/catalog_app/catalog_app.wsgi
    <Directory /var/www/catalog_app/catalog_app/>
        Order allow,deny
        Allow from all
    </Directory>
</VirtualHost>

sudo a2ensite catalog_app
sudo apache2ctl restart
 sudo service apache2 restart



## Install python modules
sudo apt-get install python-pip
sudo apt-get install virtualenv
sudo virtualenv venv
source venv/bin/activate
sudo chown -R grader:grader venv/
pip install -r requirements.txt

# Google
Add authorized domain ??? add more info ec2-3.16.230.142.us-east-2a.compute.amazonaws.com
Add authorized JavaScript origins - https://ec2-3.16.230.142.us-east-2a.compute.amazonaws.com
https://ec2-3.16.230.142.us-east-2a.compute.amazonaws.com
https://3.16.230.142
download json file 
copy the contents and replace the contents in the client_secret.json file
copy the clientid from the json file
nano templates/login.html
paste the clientid into the data-clientid field

## Change the server timezone to UTC
Run **sudo dpkg-reconfigure tzdata**
Select **None of the above** and hit enter
Select **UTC** and hit enter
#???? add requirements.txt to base project

## Disable default site
sudo a2dissite 000-default.conf
sudo service apache2 reload

http://3.16.230.142/

## Folder Structure
 * /var/www/catalog_app/catalog_app/
 * /var/www/catalog_app/catalog_app/__init__.py - main application
 * /var/www/catalog_app/catalog_app/database_setup.py - initialization of database
 * /var/www/catalog_app/catalog_app/category_books.py - populates database with sample data
 * /var/www/catalog_app/catalog_app/category.db - database created from database_setup.py
 * /var/www/catalog_app/catalog_app/client_secrets.json - secrets file (you provide)
 * /var/www/catalog_app/catalog_app/static - contains css file
 * /var/www/catalog_app/catalog_app/templates - contains html files
 


# Resources
* https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html#retrieving-the-public-key-windows
* https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/managing-users.html
* https://www.google.com/search?q=configure+linux+local+time+to+utc&oq=configure+linux+local+time+to+utc&aqs=chrome..69i57.7352j0j7&sourceid=chrome&ie=UTF-8
* https://www.digitalocean.com/community/tutorials/how-to-secure-postgresql-on-an-ubuntu-vps
* https://medium.com/coding-blocks/creating-user-database-and-adding-access-on-postgresql-8bfcd2f4a91e
* https://docs.python-guide.org/dev/virtualenvs/
* https://www.google.com/search?ei=l4d8XMqaNobGjgSsg5HABw&q=install+pip+ubuntu&oq=install+pip+&gs_l=psy-ab.1.1.0i67l5j0i20i263j0i67j0i20i263j0i67l2.4546.4546..5483...0.0..0.89.89.1......0....1..gws-wiz.......0i71.7beIQJ7ZCgo
* https://help.dreamhost.com/hc/en-us/articles/215489338-Installing-and-using-virtualenv-with-Python-2
* https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps
* http://flask.pocoo.org/docs/1.0/deploying/mod_wsgi/
* https://github.com/rrjoson/udacity-linux-server-configuration
* https://lightsail.aws.amazon.com/ls/docs/en/articles/lightsail-how-to-connect-to-your-instance-virtual-private-server
* https://thelinuxcode.com/setup-automatic-security-updates-ubuntu-16-04-17-10/
* https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04
* https://gist.github.com/shyamgupta/d8ba035403e8165510585b805cf64ee6
* https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps




--------------------
install pip virtualvenv
sudo apt-get install virtualbox
sudo apt-get install vagrant
cd dir
vagrant up

-----
git clone
copy files to /var/www/catalog_app
rename application.py to __init__.py
virtualenv venv
** add requirements to project
pip install -r requirements.txt
pip install --upgrade pip

create /var/www/catalog_app/application.wsgi

create catalog_app.conf 
nano /etc/apache2/sites-available/catalog_app.conf

update client_secrets.json with secret

sudo nano /etc/apache2/sites-enabled/000-default.conf
WSGIScriptAlias / /var/www/catalog_app/application.wsgi
sudo apache2ctl restart


Note: When you set up OAuth for your application, you will need a DNS name that refers to your instance's IP address. You can use the xip.io service to get one; this is a public service offered for free by Basecamp. For instance, the DNS name 54.84.49.254.xip.io refers to the server above.

Requirement already satisfied: Werkzeug==0.14.1 in /usr/local/lib/python2.7/dist-packages (from -r requirements.txt (line 27)) (0.14.1)

sudo chown -R ubuntu:ubuntu catalog_app

sudo a2ensite catalog_app
sudo service apache2 reload
sudo chown -R grader:grader catalog_app

source venv/bin/activate $ sudo chmod -R 777 venv

apt-get -qqy install make zip unzip postgresql
sudo su - postgres
psql
create user category with password 'category';
alter user category createdb;
create database category with owner category;
\c category
grant all on schema public to category;
grant all on schema public to catalog;
\q 
exit

???
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
???

sudo adduser category
sudo ls /etc/sudoers.d
sudo cp /etc/sudoers.d/grader /etc/sudoers.d/catalog
sudo nano /etc/sudoers.d/catalog
change grader to catalog
psql

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public to category;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public to category;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public to category;

sudo chown -R category:category catalog_app
sudo chmod 775 catalog_app