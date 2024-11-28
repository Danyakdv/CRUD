class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@db/cars'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your_secret_key'
    SECRET_KEY = 'your_secret_key'