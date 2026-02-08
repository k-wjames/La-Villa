import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "reservations.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "your-secret-key"
    # Flask-Mail settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'tera.jobs.ke@gmail.com'     
    MAIL_PASSWORD = 'dfmz mefi yqyk rwbg'           
    MAIL_DEFAULT_SENDER = ('LaVilla Bookings', 'tera.jobs.ke@gmail.com')

# 587