from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
load_dotenv()

def get_engine():
    engine = create_engine("postgresql://{0}:{1}@localhost:5432/{2}".format(
        os.getenv("DB_USER"),os.getenv("DB_PASSWORD"),os.getenv("DB_NAME")
    ))
    return engine


if __name__=="__main__":
    pass