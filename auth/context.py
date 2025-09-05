from typing import Optional
from flask import request
from extensions import db
from auth.auth import decode_token
from domains.user.models import User

# class RequestContext:
#   user: Optional[User]
#
#   def __init__(self):
#     self.user = None
#     auth = request.headers.get("Authorization", "")
#     if auth.startswith("Bearer "):
#       token = auth.removePrefix("Bearer ".strip())
#       try:
#         payload = decode_token(token)
#         if payload.get("type") != "access":
#           return
#         uid = payload.get("sub")
#         if uid:
#           self.user = db.session.get(User, int(uid))
#       except Exception:
#         pass

class RequestContext:
  request: any
  user: Optional[User]


def get_context():
  token = request.headers.get("Authorization", "").removeprefix("Bearer ").strip()
  if token:
    try:
      payload = decode_token(token)
      user = User.query.get(payload['sub'])
    except Exception as e:
      user = None
  else:
    user = None
  return RequestContext(request=request, user=user)






# class Context:
#     request: any
#     user: Optional[dict] = None  # or your User model
#
#
# def get_context():
#   token = request.headers.get("Authorization", "").removeprefix("Bearer ").strip()
#   user = None
#   if token:
#     try:
#       payload = decode_jwt(token)
#       user = get_user_by_id(payload["sub"])
#     except Exception:
#       user = None
#   return Context(request=request, user=user)
