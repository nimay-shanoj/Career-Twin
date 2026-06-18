import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'career-twin-secret-key-12345'
    DATABASE_URL = os.environ.get('DATABASE_URL')
    VERCEL_ENV = os.environ.get('VERCEL')

    if DATABASE_URL:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    elif VERCEL_ENV:
        SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/careertwin.db'
    else:
        SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://Aditya:Bigcola69@localhost/careertwin'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    if VERCEL_ENV:
        UPLOAD_FOLDER = os.path.join('/tmp', 'uploads')
    else:
        UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size
