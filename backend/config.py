import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env", override=True)

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "portfolio_secret_kathiresan_2026")

    # Database Configuration: MySQL (via DATABASE_URL or discrete DB_* env vars) or SQLite fallback
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT", "3306")
    db_name = os.getenv("DB_NAME")

    if os.getenv("DATABASE_URL"):
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    elif db_user and db_host and db_name:
        pwd_part = f":{db_password}" if db_password else ""
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_user}{pwd_part}@{db_host}:{db_port}/{db_name}"
    else:
        # Check if running in a serverless environment (e.g. Vercel) where root is read-only
        if os.path.exists("/tmp"):
            db_file_path = Path("/tmp/portfolio.db")
        else:
            db_file_path = BASE_DIR / "portfolio.db"
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_file_path.as_posix()}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CORS_ORIGIN = os.getenv("CORS_ORIGIN", "*")
    PORT = int(os.getenv("PORT", 5000))
    DEBUG = os.getenv("FLASK_DEBUG", "1") == "1"

    # Standardized Mail Configuration (Supports MAIL_*, EMAIL_*, and MAIL_RECEIVER aliases)
    MAIL_HOST = os.getenv("MAIL_HOST") or os.getenv("EMAIL_HOST", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT") or os.getenv("EMAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", os.getenv("EMAIL_USE_TLS", "True")).lower() in ("true", "1", "t")
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", os.getenv("EMAIL_USE_SSL", "False")).lower() in ("true", "1", "t")
    MAIL_USERNAME = (os.getenv("MAIL_USERNAME") or os.getenv("EMAIL_USERNAME", "")).strip()
    MAIL_PASSWORD = (os.getenv("MAIL_PASSWORD") or os.getenv("EMAIL_PASSWORD", "")).strip()
    MAIL_TO = (os.getenv("MAIL_RECEIVER") or os.getenv("MAIL_TO") or os.getenv("EMAIL_TO", "kathiresantoto@gmail.com")).strip()
    MAIL_FROM = (os.getenv("MAIL_FROM") or os.getenv("EMAIL_FROM", f"Kathiresan K Portfolio <{MAIL_TO}>")).strip()
