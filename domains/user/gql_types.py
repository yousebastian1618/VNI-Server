import strawberry

@strawberry.type
class GQLUser:
  id: strawberry.ID
  email: str

@strawberry.type
class AuthPayload:
  access_token: str
  refresh_token: str
  token_type: str = "Bearer"
  user: GQLUser

@strawberry.input
class UserLoginInput:
  email: str
  password: str

@strawberry.input
class UserCreateInput:
  email: str
  password: str

@strawberry.input
class UserUpdateInput:
  email: str
  password: str