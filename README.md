# flask-mongo
Web application created using Flask framework and MongoDB. This is a skeleton project integrating the Flask framework with MongoDB unlike using traditional relational databases like SQLlite3.

## App Functions
The app contains 2 main functionalities:
- Login
- Registration

## Some required files
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
- [Flask PyMongo documentation](https://flask-pymongo.readthedocs.io/en/latest/)
