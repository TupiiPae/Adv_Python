import os

class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:123456@localhost:3306/studio_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
