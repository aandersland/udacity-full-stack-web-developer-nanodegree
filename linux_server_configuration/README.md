# Overview
This project is focused on taking a base installation of an Ubuntu 16.04 server and prepare it to be hosted on AWS.
    
* Install required libraries
* Secure the server from attack vectors
* Install and configure the database server
* Deploy an existing web application [Project 2 - Catalog App](https://github.com/aandersland/udacity-full-stack-web-developer-nanodegree/tree/master/catalog_app)

The running application cane be seen here: http://3.16.230.142/

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
This section will create the SSH keys and apply them on the server.
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

## Setup Putty SSH connection
This section will setup an SSH connection to the new server.
1. Download and Start the Putty Configuration app
2. Enter the public ip address to your Catalog_App **3.16.230.142**
3. Change the port to **2200**
4. On the left panel click on 'SSH' and then 'Auth'
5. On the right panel browse to the **grader_private** file you created earlier
6. On the left panel click on 'Session'
7. Enter a name in the Saved Session box **grader**
8. Click on Save and then Open
9. Click on 'yes' on the pop up window
10. Enter username / password

##Configure UFW Firewall
This section will configure the server firewall to limit only necessary access and limit attack vectors for unauthorized attempts.
1. Run **sudo ufw default deny incoming**
2. Run **sudo ufw default allow outgoing**
3. Run **sudo ufw allow 2200/tcp**
4. Run **sudo ufw allow www**
5. Run **sudo ufw allow 123/udp**
6. Run **sudo ufw deny 22**
7. Run **sudo ufw enable**
8. Type in Y for the warning that comes up.
9. Run **sudo ufw status**
10. Your output should look like this:
    * Status: active
    
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
11. Run **exit**

## Update Lightsail instance - disable port 22
This section will disable the normal SSH port on our server instance.
1. Click on your 'Catalog_App' instance
2. Click on 'Networking'
3. Delete the following firewall rule:
    * **SSH - TCP - 22**
4. Click 'Save'

## Update server packages
This section will install the necessary server/library packages. 
1. Run **sudo apt-get update**
2. Run **sudo apt-get upgrade**
3. Run **sudo apt-get install postgresql postgresql-contrib**
4. Run **sudo apt-get install apache2**
    * In a web browser type in your public ip address **3.16.230.142**
    * You should see the "Apache2 Ubuntu Default Page"
5. Run **sudo apt-get install libapache2-mod-wsgi python-dev**
6. Run **sudo apt-get install python-pip**
7. Run **sudo apt-get install virtualenv**

##Configure and setup database
This section will setup access for our catalog_app user and create an empty database for use.
1. Run **sudo su - postgres**
2. Run **psql**
3. Run **create role catalog_app with login password 'catalog_app';**
4. Run **alter role catalog_app createdb;**
5. Run **\q**
6. Run **exit**
7. Run **su - catalog_app**
8. Run **createdb catalog_app**

##Setup application and reconfigure
This section will move our application to our server and update it to work with postgresql and the apache/wsgi service.
1. Run **cd /var/www/**
2. Run **sudo git clone https://github.com/aandersland/udacity-full-stack-web-developer-nanodegree.git catalog_app**
3. Run **sudo chown -R grader:grader catalog_app/**
4. Run **cd /var/www/catalog_app/catalog_app**
5. Run **mv application.py __init__.py**
6. Run **nano __init__.py** and update the following:
    * Comment this out - CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
    * Add this line to replace it - **CLIENT_ID = json.loads(open('/var/www/catalog_app/catalog_app/client_secrets.json', 'r').read())['web']['client_id']**
    * Comment this out - engine = create_engine('sqlite:///category.db') 
    * Add this line to replace it - **engine = create_engine('postgresql://catalog_app:password@localhost/catalog_app')**
    * Note you will need to replace 'password' with the actual password you created.
    * Comment this out - app.debug = True
    * Comment this out - app.run(host='0.0.0.0', port=5000, threaded=False)
    * Add this line to replace it - **app.run()**
7. Run **nano database_setup.py** and update the following:
    * Comment this out - engine = create_engine('sqlite:///category.db')
    * Add this line to replace it - **engine = create_engine('postgresql://catalog_app:password@localhost/catalog_app')**
    * Note you will need to replace 'password' with the actual password you created.
8. Run **nano category_books.py**
    * Comment this out - engine = create_engine('sqlite:///category.db')
    * Add this line to replace it - **engine = create_engine('postgresql://catalog_app:password@localhost/catalog_app')**
    * Note you will need to replace 'password' with the actual password you created.

## Install python modules
This section will detail how to setup a virtual env and install the pre-requisite libraries
1. Run **sudo virtualenv venv**
2. Run **source venv/bin/activate**
3. Run **sudo chown -R grader:grader venv/**
4. Run **pip install -r requirements.txt**

##Populate database with data
This section will detail the steps to setup the database with sample data.
1. Run **python database_setup.py**
2. Run **python category_books.py**
3. Run **python __init__.py**
    * The application should be running without errors in the command line.
4. Type CTRL+C to stop the application
5. Type deactivate to exit the virtual environment.

## Enable virtual host
This section will setup the Apache configurations for WSGI.
1. Run **sudo nano /etc/apache2/mods-enabled/wsgi.conf**
    * Under the WSGIPythonPath add **WSGIPythonPath /var/www/catalog_app/catalog_app/venv/lib/python2.7/site-packages**
2. Save the file. 
3. Run **sudo nano /etc/apache2/sites-available/catalog_app.conf**
    * Add the following to the file or copy the same file in this directory to the server instance.
**<VirtualHost *:80>
    ServerName 3.16.230.142
    ServerAlias ec2-3.16.230.142.us-east-2a.compute.amazonaws.com
    WSGIScriptAlias / /var/www/catalog_app/catalog_app/catalog_app.wsgi
    <Directory /var/www/catalog_app/catalog_app/>
        Order allow,deny
        Allow from all
    </Directory>
</VirtualHost>**
4. Run **sudo a2ensite catalog_app**
5. **sudo service apache2 restart**


# Update Google OAuth
This section will list the changes that are needed to the Google OAuth configuration.
1. Login to https://console.developers.google.com
2. Under the OAuth consent screen for your application add this to the authorized domains **ec2-3.16.230.142.us-east-2a.compute.amazonaws.com**
3. Under the OAuth client id add the following under the 'Authorized Javascript origins':
    * https://ec2-3.16.230.142.us-east-2a.compute.amazonaws.com
    * https://3.16.230.142
    * https://3.16.230.142.xip.io
4. Save the changes
5. Under the OAuth client id add the following under the 'Authorized redirect URLs':
	* https://ec2-3.16.230.142.us-east-2a.compute.amazonaws.com/
	* https://3.16.230.142.xip.io/catalog/
6. Save the changes
7. Download json file for this client id 
8. Copy the contents of the file
9. Run **nano /var/www/catalog_app/catalog_app/client_secret.json** and replace the contents in the file 
10. Copy the clientid value from the json file
11. Run **nano /var/www/catalog_app/catalog_app/templates/login.html** and replace the existing clientid into the data-clientid field

## Change the server timezone to UTC
This section will update the timestamp of the server to UTC
1. Run **sudo dpkg-reconfigure tzdata**
2. Select **None of the above** and hit enter
3. Select **UTC** and hit enter

## Disable default site
This section will disable the default Apache site for security.
1. Run **sudo a2dissite 000-default.conf**
2. Run **sudo service apache2 reload**

## Folder Structure
 * /var/www/catalog_app/catalog_app/
 * /var/www/catalog_app/catalog_app/__init__.py - main application
 * /var/www/catalog_app/catalog_app/database_setup.py - initialization of database
 * /var/www/catalog_app/catalog_app/category_books.py - populates database with sample data
 * /var/www/catalog_app/catalog_app/category.db - database created from database_setup.py
 * /var/www/catalog_app/catalog_app/client_secrets.json - secrets file (you provide)
 * /var/www/catalog_app/catalog_app/static - contains css file
 * /var/www/catalog_app/catalog_app/templates - contains html files

## Resources
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
