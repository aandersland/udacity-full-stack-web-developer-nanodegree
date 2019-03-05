## Overview
This project is focused on developing a web application with a backend database. It will include user registration, and authentication system. Users will be able to create, edit, and delete items if they are logged in.
* RESTful web application
* Python Flask framework
* Third-party OAuth authentication
* HTTP methods
* Database CRUD operations
* JSON endpoints

## Setup
You will need the following installed on your machine: 
1. Install VirtualBox - https://www.virtualbox.org/wiki/Downloads
2. A linux based virtual machine if you do not have linux -  https://www.vagrantup.com/
3. A copy of the Vagrant file from Udacity located in this repository.
4. The python files in this repository.
5. Your folder structure should look like the example below.
6. Once your folders are setup navigate to the root_folder and run the command **vagrant up** to setup your virtual machine.
7. After it finishes installing the components you can run **vagrant ssh** to access the virtual machine.
8. Once in the vm run **cd /vagrant**. This will navigate to the shared folder on your computer where the files are located.
9. Follow the steps below for Create Google OAUTH Credentials below before proceeding further.
9. Next run this command ** python database_setup.py** to create the category database.
10. Next run this command ** python category_books.py** to populate the category database with sample data.
11. Finally run the command **python application.py** to start the website. Python 2.7 was used in the creation of this script.
12. In your web browser navigate to the following url: http://localhost:5000/

## Create Google OAUTH Credentials
1. Login to the following site: https://console.developers.google.com
2. Click on **Create Project** and populate the information.
3. Click on **Credentials** on the left nav panel.
4. Create an **OAuth Client ID**.
5. Populate the following on the consent screen:
* Application name = **Catalog App**
* Support email = **your email**
6. Choose **Web Application** when available.
5. Click on Save / Submit for verification and follow the instructions.
7. Once the credentials are created click on the edit icon.
8. On the next page enter the following: 
* Authorized JavaScript **http://localhost:5000**
* Authorized redirect URIs **http://localhost:5000/catalog/**
9. Click save
10. Click on the download JSON file and replace the client_secrets.json file in this project.
11. Copy the **client_id** value in the client_secrets file and replace the **data-clientid** value in the login.html file.


## Folder Structure
 * root_folder/catalog_app
 * root_folder/catalog_app/application.py - main application
 * root_folder/catalog_app/database_setup.py - initialization of database
 * root_folder/catalog_app/category_books.py - populates database with sample data
 * root_folder/catalog_app/category.db - database created from database_setup.py
 * root_folder/catalog_app/client_secrets.json - secrets file (you provide)
 * root_folder/catalog_app/Vagrantfile - file for the creation of a vm
 * root_folder/catalog_app/static - contains css file
 * root_folder/catalog_app/templates - contains html files
 
## JSON Endpoints
* /categories/api - list all categories
* /books/api - list all books
* /category/books/api - list all category books
* /users/api - list all users

## Resources
* https://htmlcheatsheet.com/css/
* https://www.cssbasics.com/
* https://www.w3schools.com
* https://docs.sqlalchemy.org/en/latest/core/defaults.html
* https://html-css-js.com/css/editor/
* https://htmlcheatsheet.com/css/
* https://www.cssbasics.com/introduction-to-css/
* http://jinja.pocoo.org/docs/2.10/templates/
* https://medium.freecodecamp.org/css-grid-a-simple-layout-design-tutorial-5312a4a8bcaf
* https://alligator.io/css/align-justify/
* https://www.w3schools.com/tags/tag_textarea.asp
* https://console.developers.google.com/apis
