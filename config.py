import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'bardzo-tajny-klucz-studencki'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///project.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False