from typing import Optional
from graphql import GraphQLError
from sqlalchemy.orm import Session
from auth.auth import create_access_token, create_refresh_token, get_user_from_token
from helper.index import to_uuid
from .gql_types import AuthPayload
from .models import User
from extensions import db

def get_user_by_token():
  user = get_user_from_token()
  if user is None: return None
  db_user = User.query.get(to_uuid(user['id']))
  if not user:
    return None
  return db_user

def create_user(email, password) -> User:
  new_user = User(email=email)
  new_user.set_password(password)
  db.session.add(new_user)
  db.session.commit()
  return new_user

def update_user(uid, email: str, password: str) -> Optional[User]:
  target_user = User.query.get(uid)
  if not target_user:
    return None
  if email is not None:
    target_user.email = email
  if password is not None:
    target_user.set_password(password)
  db.session.commit()
  return target_user

def delete_user(uid) -> bool:
  target_user = User.query.get(uid)
  if not target_user:
    return False
  db.session.delete(target_user)
  db.session.commit()
  return True

def login(email, password) -> AuthPayload:
  session: Session = db.session
  user: User | None = session.query(User).filter(User.email == email).first()
  if not user or not user.check_password(password):
    raise GraphQLError(
      "Invalid email or password",
      extensions={"code": "BAD_REQUEST", "status": 400}
    )
  access = create_access_token(sub=str(user.id), extra={"id": str(user.id), "email": user.email})
  refresh = create_refresh_token(sub=str(user.id))
  user = User.query.get(user.id)
  return AuthPayload(
    access_token='Bearer ' + access,
    refresh_token=refresh,
    user=user,
  )

