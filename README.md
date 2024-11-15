#Prerequisites

Ensure you have Python and Flask installed.

#Database Setup

Reset Database: Delete the used_cars.db file if you want to start with a fresh database.

Initialize Database: Run init_db.py to create a new database.

#Starting the Application

Run boundary.py to start the website on local host.


Default Admin Credentials

Username: admin1
Password: admin123

#Testing

Install Testing Packages: For testing, install pytest and Flask-Testing.

pip install pytest Flask-Testing

Run Test script: Execute test_app.py using one of the following commands:

python -m pytest test_app.py

or

pytest test_app.py

#For populating the database with 100+ records:

run init_testdb.py
