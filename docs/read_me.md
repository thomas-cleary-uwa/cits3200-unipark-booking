# cits3200-unipark-booking
A car bay booking web application for UWA's UniPark office
<br>

## Linting
To avoid some incorrect linting when using ***pylint*** add this line to your _.vscode/settings.json_ file:

`"python.linting.pylintArgs": ["--load-plugins", "pylint_flask_sqlalchemy", "pylint_flask"]`
<br><br>

## Walkthroughs

0. [Setup](https://youtu.be/_bJY0cp90w4)
1. [What happens when you run the app](https://youtu.be/aZ9d8qhxnsc)
2. [Working with Flask and a Database](https://youtu.be/tXokeftmGkE)
3. [Explanation the the _app_ package](https://youtu.be/pCmkMkBuaEE)
4. [Explanation of the unit tests](https://youtu.be/NuK26NFPl1E)
<br><br>

## To Run the Flask App


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

### 3.b Install wkhtmltopdf
Install this program to be able to use *pdfkit* to generate reservation signs
https://wkhtmltopdf.org/

If you want to disable pdf generation and confirmaton emails, comment out this section of *bookings/helpers.py*

```
if not no_email:
    bay = new_booking.bay

    lot_num = bay.lot.lot_number
    bay_num = bay.bay_number
    
    thr = Thread(target=generate_reservation_sign, args=[
        current_app._get_current_object(),
        new_booking,
        bay_num,
        lot_num,
        User.query.get(current_user.id)
    ])
    thr.start()
```


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

- ADMIN_EMAIL=**(eg. uni.park@uwa.edu.au)**
- ADMIN_PASSWORD=**(atleast 8 characters, eg. admin1234)**

- TEST_USER_EMAIL=**(your email address)** (used with run_fresh_app.py -u)
- TEST_USER_PASSWORD=**(eg. user1234)**

- MAIL_USERNAME=unipark.mailtest@gmail.com
- MAIL_PASSWORD=uniparkt3st
- MAIL_DEFAULT_SENDER=unipark.mailtest@gmail.com

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

There are options being added to the run_fresh_app.py script so use 

`$ python run/run_fresh_app.py --help`

or

`$ python run/run_fresh_app.py --h`

to see options

For example, 

`$ python run/run_fresh_app.py --add-user`

will run a _fresh_ version of the app with a regular user inserted already.



### 6. Finally
Navigate to **http://localhost:5000/** on your chosen browser
