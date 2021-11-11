class Config(object):
    TESTING = False

    SQLALCHEMY_DATABASE_URI = "sqlite:///gpios.db"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

