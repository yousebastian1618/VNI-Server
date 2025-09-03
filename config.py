import os
from dotenv import load_dotenv

load_dotenv()

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
  JWT_ACCESS_TTL_MIN = os.environ.get("JWT_ACCESS_TTL_MIN")
  JWT_REFRESH_TTL_DAYS = os.environ.get("JWT_REFRESH_TTL_DAYS")
  JWT_ALG = os.environ.get("JWT_ALG")
  JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")