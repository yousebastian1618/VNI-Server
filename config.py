import os
from dotenv import load_dotenv

load_dotenv()


def as_bool(v, default=False):
  if v is None:
    return default
  return str(v).strip().lower() in ("1", "true", "yes", "y", "on")


class Config:
  SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///vni.db")
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  JSON_SORT_KEYS = False,


  BUCKET = os.environ.get("BUCKET")
  CLOUDFLARE_ACCOUNT_ID = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
  CLOUDFLARE_ACCESS_KEY_ID = os.environ.get("CLOUDFLARE_ACCESS_KEY_ID")
  CLOUDFLARE_SECRET_ACCESS_KEY = os.environ.get("CLOUDFLARE_SECRET_ACCESS_KEY")
  END_POINT_URL = os.environ.get("END_POINT_URL")
  CLOUDFLARE_TOKEN = os.environ.get("CLOUDFLARE_TOKEN")
  JURISDICTION_SPECIFIC_ENDPOINTS = os.environ.get("JURISDICTION_SPECIFIC_ENDPOINTS")


  JWT_ACCESS_TTL_MIN = int(os.environ.get("JWT_ACCESS_TTL_MIN"))
  JWT_REFRESH_TTL_DAYS = int(os.environ.get("JWT_REFRESH_TTL_DAYS"))
  JWT_ALG = os.environ.get("JWT_ALG")
  JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")


  MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
  MAIL_PORT = int(os.environ.get("MAIL_PORT", "587"))
  MAIL_USE_TLS = as_bool(os.environ.get("MAIL_USE_TLS", "true"))
  MAIL_USE_SSL = as_bool(os.environ.get("MAIL_USE_SSL", "false"))
  MAIL_USERNAME = os.environ.get("ADMIN_EMAIL")
  MAIL_PASSWORD = os.environ.get('SMTP_APP_PASSWORD')
  MAIL_DEFAULT_SENDER = "Vitali Inquiry"
  ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL")