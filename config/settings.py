from decouple import config
import motor.motor_asyncio


def settings(expire_time=60 * 12):
    # to get a string like this run:
    # openssl rand -hex 32
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = expire_time

    return SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


def get_db_users():
    client = motor.motor_asyncio.AsyncIOMotorClient(config("DB_URL"))
    db = client[config("DATABASE_USER")]
    return db


def get_db_projects():
    client = motor.motor_asyncio.AsyncIOMotorClient(config("DB_URL2"))
    db = client[config("DATABASE_PROJECTS")]
    return db
