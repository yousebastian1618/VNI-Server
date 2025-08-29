import strawberry
from graphql import GraphQLError
from .gql_types import GQLBlog
from typing import List
from .models import Blog

@strawberry.type
class BlogQueries:
  @strawberry.field
  def blogs(self, limit: int = 20, offset: int = 0) -> List[GQLBlog]:
    rows = Blog.query.order_by(Blog.created_at.desc()).offset(offset).limit(limit)
    return [
      GQLBlog(
        id=b.id,
        title=b.title,
        subtitle=b.subtitle,
        main_image=b.main_image,
        index=b.index
      ) for b in rows
    ]

  @strawberry.field
  def blog(self, uid: strawberry.ID) -> GQLBlog:
    blog = Blog.query.get(uid)
    if not blog:
      raise GraphQLError(
        "Blog does not exists",
        extensions={"code": "NOT_FOUND", "status": 404}
      )
    return GQLBlog(
      id=blog.id,
      title=blog.title,
      subtitle=blog.subtitle,
      main_image=blog.main_image,
      index=blog.index
    )

  @strawberry.field
  def count_blogs(self) -> int:
    return Blog.query.count()