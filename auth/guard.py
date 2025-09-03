from functools import wraps
from graphql import GraphQLError
from strawberry.types import Info

def login_required(resolver):
  @wraps(resolver)
  def wrapper(*args, info: Info, **kwargs):
    if not getattr(info.context, "user", None):
      raise GraphQLError(
        "You are not authenticated",
        extensions={"code": "NOT_AUTHENTICATED", "status": 401}
      )
    return resolver(*args, info=info, **kwargs)
  return wrapper
