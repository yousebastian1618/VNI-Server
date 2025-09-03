from typing import Optional
import strawberry
from domains.user.gql_types import GQLUser
from . import services as user_service

def to_gql_user(user) -> GQLUser:
  return GQLUser(
    id=user.id,
    email=user.email,
  )

@strawberry.type
class UserQueries:
  @strawberry.field
  def get_user_by_token(self) -> Optional[GQLUser]:
    user = user_service.get_user_by_token()
    if user is None: return None
    return to_gql_user(user)