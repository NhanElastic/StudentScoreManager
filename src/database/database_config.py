from dotenv import load_dotenv
import os

load_dotenv()
USERNAME = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
DATABASE = os.getenv("DB_NAME")

class Settings:
    DATABASE_URL = f"mysql+aiomysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

settings = Settings()