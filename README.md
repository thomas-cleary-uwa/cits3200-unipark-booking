# cits3200-unipark-booking
A car bay booking web application for UWA's UniPark office
<br><br>

**NOTE: PLEASE USE DEV BRANCH AND DO NOT PUSH TO MAIN**

## To Run the Flask App

### 1. Create a Python Virtual Environment
Inside ./flask-app run the command

`$ python -m venv venv`

NOTE: Your system may have python aliased as something other than `python`

### 2. Activate the Virtual Environment
`$ source venv/bin/activate`

NOTE: On windows

`$ venv\Scripts\activate`

### 3. Install Requirements
`$ pip install -r requirements.txt`

NOTE: Your system may have pip aliased as something other than `pip`

**NOTE: Before attempting to run the flask app, please change the 
*python.pythonPath* setting in .vscode/settings.json to your virtual environment's python path. This can be found by running the command (linux / macOS)**  

`$ which python`

### 4. Add .env File
`$ touch .env`

(Command only on linux / macOS, will need to manually create file manually on Windows)

This is the file that the flask application will take environment variables from.

Currently need values for:
- FLASK_APP=unipark_booking.py
- FLASK_CONFIG=**(config name from config.py, eg. development)**
- FLASK_ENV=**(development or production)**
- SECRET_KEY=**(secret key used for encryption eg. youwillneverguessthis)**
- ADMIN_EMAIL=**(eg. test@uwa.edu.au)**
- ADMIN_PASSWORD=**(eg. admin)**

### 5. Create a local database file for the app 
To run the app you need a local instance of the database. 

#### Option 1: Manual Option
To create this file run the following two commands from /flask-app

`$ flask db migrate`  
`$ flask db upgrade`

#### Option 2: Automated Option
To automatically run the above commands and start the application simply run from /flask-app

`$ python run/run_fresh_app.py`

### 6. Run the Application
Before running the application, consider running the unit tests

`$ flask test`

To start the Flask app, run this command from inside /flask-app

`$ flask run`

Optionally to run the app with a fresh/new instance of the database run this command from /flask-app

`$ python run/run_fresh_app.py`

and navigate to **http://localhost:5000/** on your chosen browser
