from functools import wraps
from flask import request
from graphql import GraphQLError

from auth.auth import decode_token
from domains.user.models import User
from extensions import db


def login_required(resolver):
  @wraps(resolver)
  def wrapper(*args, **kwargs):
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
      token = auth.split("Bearer ")[1]
      try:
        payload = decode_token(token)
        if payload.get("type") != "access":
          return None
        uid = payload.get("sub")
        if uid:
          user = db.session.get(User, uid)
          if user is None:
            raise GraphQLError(
              "Unauthorized",
              extensions={"code": "NOT_AUTHORIZED", "status": 401}
            )
      except Exception as e:
        raise GraphQLError(
          "Unauthorized",
          extensions={"code": "NOT_AUTHORIZED", "status": 401}
        )
    else:
      raise GraphQLError(
        "Unauthorized",
        extensions={"code": "NOT_AUTHORIZED", "status": 401}
      )
    return resolver(*args, **kwargs)
  return wrapper
