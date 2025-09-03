from typing import Optional
from flask import request
from extensions import db
from auth.auth import decode_token
from domains.user.models import User

class RequestContext:
  user: Optional[User]

  def __init__(self):
    self.user = None
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
      token = auth.removePrefix("Bearer ".strip())
      try:
        payload = decode_token(token)
        if payload.get("type") != "access":
          return
        uid = payload.get("sub")
        if uid:
          self.user = db.session.get(User, int(uid))
      except Exception:
        pass
