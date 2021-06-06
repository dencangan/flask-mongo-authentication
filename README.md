# flask-mongo
This is a skeleton web application integrating the Flask framework with MongoDB unlike using traditional relational databases like SQlite3. This project assumes that you have some basic knowledge in MongoDB (PyMongo collections) and Flask.

## App Overview
The app covers user authentication, registration, password encryption and storage with MongoDB. There are 3 pages in the app: 

<b>Login Page</b>
<p align="center">
  <br>
  <img height="400" width="800" src="img/login.PNG">
  <br>
  <i>The main login page to enter credentials that will handle the validation and link redirection.</i>
</p>
<br>

<b>Registration Page</b>
<p align="center">
  <br>
  <img height="400" width="800" src="img/register.PNG">
  <br>
  <i>The registration page to handle creation/storage of user details and password encryption in MongoDB.</i>
</p>
</p>
<br>

<b>Home Page</b>
<p align="center">
  <br>
  <img src="img/home.PNG">
  <br>
  <i>The home page after the user has been authenticated. A logout button is set to log the user out back to the login page.</i>
</p>
</p>
<br>

## How It Works
The main modules to look at is 'models.py' and 'auth/routes.py'. As we are using a noSQL database, we have to build our 'User' object slightly differently from the conventional SQL style.

From [Miguel Grinberg's](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins) tutorial on using Flask-login:

> The Flask-Login extension works with the application's user model, and expects certain properties and methods to be implemented in it. 
The four required items are listed below:
> - is_authenticated: a property that is True if the user has valid credentials or False otherwise.
> - is_active: a property that is True if the user's account is active or False otherwise.
> - is_anonymous: a property that is False for regular users, and True for a special, anonymous user.
> - get_id(): a method that returns a unique identifier for the user as a string.

### User object
These are defined as static methods in the object. Our database collection name is called "user_details".
```python
class User:
    """User object that can be manipulated with mongo."""

    def __init__(self, username=None, email=None, password=None):
        self.username = username
        self.email = email
        self.password = password
        # Your mongo URI defined in config.py
        self.db = MongoClient(Config.MONGO_URI)["Users"]

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.username
```

### User Registration
A step is required to store the details in a dictionary (NoSQL style) before inserting it into the mongo collection (see to_dict()). The password stored in the database is of course, hashed.
```python
  def register(self):
      """Inserting user details into mongo collection."""
      self.db["user_details"].insert_one(self.to_dict())
      print(f"{self.to_dict()} entry created.")

  def to_dict(self):
      """Transform to dict to insert into mongo collection."""
      return {
          "name": self.username,
          "email": self.email,
          # Storing hashed password, you should NEVER store the password itself in the database
          "password": self.password_hash,
      }
```

### Password Encryption
As for password encryption, we will be using the package [Werkzeug](https://werkzeug.palletsprojects.com/en/1.0.x/) with their inbuilt security hashing functions.
```python
@classmethod
def set_password(cls, password):
    """Hashing the password with Werkzeug hash generator."""
    cls.password_hash = generate_password_hash(password)

@staticmethod
def check_password(hashed_password, password):
    """Validating the hashed password."""
    return check_password_hash(hashed_password, password)
```

### Login Authentication - auth/routes.py
This function handles the authentication and redirects user to the home page if the entered credentials are correct. Basically it will look up the details of the user in the database (get_by_username) that is logging in, and then apply a Werkzeug security function (check_password) to check the hashed password in the database matches the user entered password. 
```python
@login.user_loader
def load_user(username):
    user = User().get_by_username(username)
    if not user:
        return None
    return User(username=user["name"])

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Main login logic."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User().get_by_username(username=login_form.username.data)
        if user is not None and User.check_password(hashed_password=user["password"], 
        password=login_form.password.data):
            print("Password validated.")
            print(f"ID: '{user['_id']}' - Username: '{user['name']}' logging in.")
            user_obj = User(username=user["name"])
            login_user(user_obj)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('main.index')
            return redirect(next_page)
        else:
            print(f"User '{login_form.username.data}' entered invalid credentials.")
            flash("Invalid username or password")

    return render_template('login.html', title='Sign In', login_form=login_form)
```
And there you have it, the main logic around authentication and password encryption with Flask and MongoDB.
<br>

## Some Required Files
### config.py
This is the config file that sits at the first level of the project along with the main app module. This config file is not committed as it contains confidential information like secret keys and database credentials. To get an idea, the module should look like this.
```python
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "some-secret-key"
    MONGO_URI = "some-mongo-credentials"
```

### .flaskenv
Since environment variables aren't remembered across terminal sessions, you may find tedious to always have to set the FLASK_APP environment variable when you open a new terminal window. With a .flaskenv file, Flask allows you to register environment variables that you want to be automatically imported when you run the flask command.

## Resources
The below are links to the resources used to make this project possible.
- [Comprehensive Flask tutorial by Miguel Grinberg](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [Stack Overflow discussion on MongoDB use with Flask](https://stackoverflow.com/questions/54992412/flask-login-usermixin-class-with-a-mongodb)
- [Werkzeug documentation](https://werkzeug.palletsprojects.com/en/1.0.x/)
- [Flask PyMongo documentation](https://flask-pymongo.readthedocs.io/en/latest/)
