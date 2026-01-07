import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "walletwise-dev-key")
    DB_PATH = os.environ.get("DB_PATH", os.path.join(BASE_DIR, "walletwise.sqlite"))
