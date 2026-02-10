import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "reservations.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'mail.lavilla.co.ke'
    MAIL_PORT = 465
    MAIL_USE_TLS = False          
    MAIL_USE_SSL = True 
    MAIL_USERNAME = 'reservations@lavilla.co.ke'     
    MAIL_PASSWORD = 'mw3nyEjiw@vill4'           
    MAIL_DEFAULT_SENDER = ('LaVilla Reservations', 'reservations@lavilla.co.ke')

# 587