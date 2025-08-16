# config.py
class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/db.sqlite'  # changed!
    SQLALCHEMY_TRACK_MODIFICATIONS = False
