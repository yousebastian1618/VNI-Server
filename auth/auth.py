import os
from typing import Dict, Any, Optional
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import request

load_dotenv()

def _now() -> datetime:
  return datetime.now()

def create_access_token(sub: str, extra: Optional[Dict[str, Any]]) -> str:
  payload = {
    "sub": sub,
    "type": "access",
    "iat": int(_now().timestamp()),
    "exp": int((_now() + timedelta(minutes=int(os.environ.get("JWT_ACCESS_TTL_MIN", 30)))).timestamp())
  }
  if extra:
    payload.update(extra)
  return jwt.encode(payload, os.environ.get("JWT_SECRET_KEY"), algorithm=os.environ.get("JWT_ALG", "HS256"))

def create_refresh_token(sub: str) -> str:
  payload = {
    "sub": sub,
    "type": "refresh",
    "iat": int(_now().timestamp()),
    "exp": int((_now() + timedelta(days=os.environ.get("JWT_REFRESH_TTL", 7))).timestamp())
  }
  return jwt.encode(payload, os.environ.get('JWT_SECRET_KEY'), algorithm=os.environ.get("JWT_ALG", "HS256"))

def decode_token(token: str) -> Dict[str, Any]:
  return jwt.decode(token, os.environ.get("JWT_SECRET_KEY"), algorithms=os.environ.get("JWT_ALG", "HS256"))

def get_user_from_token():
  auth = request.headers.get("Authorization", "")
  if not auth.startswith("Bearer"):
    return None
  token = auth.split(" ", 1)[1]
  try:
    payload = decode_token(token)
    return payload
  except jwt.ExpiredSignatureError:
    return None
  except jwt.InvalidTokenError:
    return None


