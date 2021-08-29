# cits3200-unipark-booking
A car bay booking web application for UWA's UniPark office
<br><br>

**NOTE: DO NOT DIRECTLY MERGE / PUSH TO MAIN OR DEV (PLEASE CREATE A PULL REQUEST**

## To Run the Flask App
*Walkthrough: https://youtu.be/_bJY0cp90w4*

### 1. Create a Python Virtual Environment
Inside ./flask-app run the command

`$ python -m venv venv`

NOTE: Your system may have python3 aliased as something other than `python`

### 2. Activate the Virtual Environment
`$ source venv/bin/activate`

NOTE: On windows

`$ venv\Scripts\activate`

### 3. Install Requirements
`$ pip install -r requirements.txt`

NOTE: Your system may have pip aliased as something other than `pip`

### 4. Add .env File
`$ touch .env` - and then edit .env in a text editor (Command only on linux / macOS)<br>
or<br>
`$ vi .env` (make sure to save the file when exiting using **:wq**<br> 
or<br>
**Manually create the file in _VSCode_**

This is the file that the flask application will take environment variables from.

Currently need values for:
- FLASK_APP=unipark_booking.py
- FLASK_CONFIG=**(config name from config.py, eg. development)**
- FLASK_ENV=**(development or production)**
- SECRET_KEY=**(secret key used for encryption eg. youwillneverguessthis)**
- ADMIN_EMAIL=**(eg. test@uwa.edu.au)**
- ADMIN_PASSWORD=**(eg. admin)**

### 5. Setup the Database and Run the Flask App
To run the app you need a local instance of the database. 

#### Option 1: Manual Option
To create the SQLite database file run the following two commands from /flask-app

`$ flask db migrate`  
`$ flask db upgrade`  

Before running the application, consider running the unit tests

`$ flask test`

To start the Flask app, run this command from inside /flask-app

`$ flask run`

#### Option 2: Automated Option
To automatically run the above commands and start the application simply run from /flask-app

`$ python run/run_fresh_app.py`

**NOTE: This script also calls `flask run`**

`$ python run/run_fresh_app.py`


### 6. Finally
Navigate to **http://localhost:5000/** on your chosen browser
