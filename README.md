# cits3200-unipark-booking
A car bay booking web application for UWA's UniPark office
<br><br>

## To Run the Flask App

### 1. Create a Python Virtual Environment
Inside ./flask-app run the command

`$ python3 -m venv venv`

NOTE: Your system may have python aliased as something other than `python3`

### 2. Activate the Virtual Environment
`$ source venv/bin.activate`

### 3. Install Requirements
`$ pip3 install -r requirements.txt`

### 4. Add .env File
`$ touch .env`

This is the file that the flask application will take environment variables from.

Currently need values for:
- FLASK_APP=unipark_booking.py
- FLASK_CONFIG=**(config name from config.py)**
- FLASK_ENV=**(development or production)**
- SECRET_KEY=**(secret key used for encryption eg. youwillneverguessthis)**

### 5. Run the Application
Run this command from inside /flask-app

`$ flask run`

and navigate to **http://localhost:5000/** on your chosen browser
