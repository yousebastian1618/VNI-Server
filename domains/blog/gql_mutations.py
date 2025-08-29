import strawberry
from graphql import GraphQLError
from .gql_types import GQLBlog, BlogCreateInput, BlogUpdateInput
from extensions import db
from .models import Blog, BlogImage, BlogParagraph
from typing import Optional


@strawberry.type
class BlogMutations:
  @strawberry.mutation
  def create_blog(self, gql_input: BlogCreateInput) -> GQLBlog:
    blog = Blog(
      title=gql_input.title,
      subtitle=gql_input.subtitle,
      main_image=gql_input.main_image,
      index=gql_input.index
    )
    db.session.add(blog)
    db.session.flush()

    if gql_input.images:
      for img in gql_input.images:
        db.session.add(
          BlogImage(
            blog_id=blog.id,
            url=img.url,
            alt_text=img.alt_text,
            index=img.index or 0
          )
        )
    if gql_input.paragraphs:
      for paragraph in gql_input.paragraphs:
        db.session.add(
          BlogParagraph(
            blog_id=blog.id,
            text=paragraph.text,
            index=paragraph.index or 0
          )
        )
    db.session.commit()
    return GQLBlog(id=blog.id, title=blog.title, subtitle=blog.subtitle, main_image=blog.main_image)


  @strawberry.mutation
  def update_blog(self, gql_input: BlogUpdateInput) -> Optional[GQLBlog]:
    blog = Blog.query.get(gql_input.id)
    if not blog:
      raise GraphQLError(
        "Blog does not exists",
        extensions={"code": "NOT_FOUND", "status": 404}
      )
    if gql_input.title is not None:
      blog.title = gql_input.title
    if gql_input.subtitle is not None:
      blog.subtitle = gql_input.subtitle
    if gql_input.main_image is not None:
      blog.main_image = gql_input.main_image
    if gql_input.index is not None:
      blog.index = gql_input.index

    if gql_input.images is not None:
      BlogImage.query.filter_by(blog_id=blog.id).delete()
      for img in gql_input.images:
        db.session.add(
          BlogImage(
            blog_id=blog.id,
            url=img.url,
            alt_text=img.alt_text,
            index=img.index or 0
          )
        )
    if gql_input.paragraphs is not None:
      BlogParagraph.query.filter_by(blog_id=blog.id).delete()
      for paragraph in gql_input.paragraphs:
        db.session.add(
          BlogParagraph(
            blog_id=blog.id,
            text=paragraph.text,
            index=paragraph.index or 0
          )
        )
    db.session.commit()
    return GQLBlog(
      id=blog.id,
      title=blog.title,
      subtitle=blog.subtitle,
      main_image=blog.main_image,
      index=blog.index
    )

  @strawberry.mutation
  def delete_blog(self, id: strawberry.ID) -> bool:
    blog = Blog.query.get(id)
    if not blog:
      raise GraphQLError(
        "Blog does not exists",
        extensions={"code": "NOT_FOUND", "status": 404}
      )
    db.session.delete(blog)
    db.session.commit()
    return True