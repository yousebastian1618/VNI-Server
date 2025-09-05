import strawberry
from auth.guard import login_required
from . import services as user_service
from domains.user.gql_types import UserCreateInput, GQLUser, UserUpdateInput, AuthPayload, UserLoginInput


def to_gql_user(user) -> GQLUser:
  return GQLUser(
    id=user.id,
    email=user.email,
  )

def to_gql_auth_payload(auth_payload) -> AuthPayload:
  return AuthPayload(
    access_token=auth_payload.access_token,
    refresh_token=auth_payload.refresh_token,
    user=to_gql_user(auth_payload.user)
  )

@strawberry.type
class UserMutations:
  @strawberry.mutation
  def create_user(self, gql_input: UserCreateInput) -> GQLUser:
    new_user = user_service.create_user(
      email=gql_input.email,
      password=gql_input.password,
    )
    return to_gql_user(new_user)

  @strawberry.mutation
  @login_required
  def update_user(self, gql_input: UserUpdateInput) -> GQLUser:
    target_user = user_service.update_user(
      gql_input.email,
      gql_input.password
    )
    return to_gql_user(target_user)

  @strawberry.mutation
  @login_required
  def delete_user(self, uid: strawberry.ID) -> bool:
    return user_service.delete_user(uid)

  @strawberry.mutation
  def login(self, gql_input: UserLoginInput) -> AuthPayload:
    auth_payload = user_service.login(gql_input.email, gql_input.password)
    return to_gql_auth_payload(auth_payload)