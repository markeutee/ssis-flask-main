
# config.py

from dotenv import load_dotenv
from pathlib import Path
import os

# ✅ Load .env file explicitly from the root directory

env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)


class Config:
    # ✅ Flask settings (optional)
    FLASK_APP = os.getenv("FLASK_APP")
    FLASK_DEBUG = os.getenv("FLASK_DEBUG")

    # ✅ MySQL settings
    SECRET_KEY = os.getenv("SECRET_KEY")
    MYSQL_DB = os.getenv("DB_NAME")
    MYSQL_USER = os.getenv("DB_USERNAME")
    MYSQL_PASSWORD = os.getenv("DB_PASSWORD")
    MYSQL_HOST = os.getenv("DB_HOST")
    MYSQL_PORT = int(os.getenv("DB_PORT"))

    # ✅ Cloudinary settings
    # ✅ Corrected Cloudinary settings (MUST match .env variable names)
    CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')
    CLOUDINARY_FOLDER = os.getenv('CLOUDINARY_FOLDER') or 'student_pics'
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    
