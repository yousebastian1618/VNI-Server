import strawberry
from auth.guard import login_required
from .gql_types import GQLBlog, BlogCreateInput, BlogUpdateInput, GQLBlogImage, GQLBlogParagraph, BlogImageUpdateInput, BlogParagraphUpdateInput
from typing import Optional
from . import services as blog_service

def to_gql_blog_image(blog_image) -> GQLBlogImage:
  return GQLBlogImage(
    id=blog_image.id,
    index=blog_image.index,
    blog_id=blog_image.blog_id
  )

def to_gql_blog_paragraph(blog_paragraph) -> GQLBlogParagraph:
  return GQLBlogParagraph(
    id=blog_paragraph.id,
    text=blog_paragraph.text,
    index=blog_paragraph.index,
    blog_id=blog_paragraph.blog_id
  )

def to_gql_blog(blog) -> GQLBlog:
  return GQLBlog(
    id=blog.id,
    title=blog.title,
    subtitle=blog.subtitle,
    created_at=blog.created_at,
    updated_at=blog.updated_at,
    index=blog.index,
    images=[to_gql_blog_image(image) for image in blog.images],
    paragraphs=[to_gql_blog_paragraph[paragraph] for paragraph in blog.paragraphs]
  )

@strawberry.type
class BlogMutations:
  @strawberry.mutation
  @login_required
  def create_blog(self, gql_input: BlogCreateInput) -> GQLBlog:
    blog = blog_service.create_blog(
      title=gql_input.title,
      subtitle=gql_input.subtitle,
      images=gql_input.images,
      paragraphs=gql_input.paragraphs
    )
    return to_gql_blog(blog)

  @strawberry.mutation
  @login_required
  def update_blog(self, gql_input: BlogUpdateInput) -> Optional[GQLBlog]:
    target_blog = blog_service.update_blog(
      uid=gql_input.id,
      title=gql_input.title,
      subtitle=gql_input.subtitle,
      images=gql_input.images,
      paragraphs=gql_input.paragraphs
    )
    return to_gql_blog(target_blog)

  @strawberry.mutation
  @login_required
  def delete_blog(self, uid: strawberry.ID) -> bool:
    blog_service.delete_blog(uid)

  @strawberry.mutation
  @login_required
  def update_blog_image(self, gql_input: BlogImageUpdateInput) -> Optional[GQLBlogImage]:
    target_blog_image = blog_service.update_blog_image(
      uid=gql_input.id,
      index=gql_input.index
    )
    return to_gql_blog_image(target_blog_image)

  @strawberry.mutation
  @login_required
  def delete_blog_image(self, uid: strawberry.ID) -> bool:
    blog_service.delete_blog_image(uid)

  # @strawberry.mutation
  # def create_blog_paragraph(self, gql_input: BlogParagraphCreateInput) -> GQLBlogParagraph:
  #   blog_paragraph = blog_service.create_blog_paragraph(
  #     gql_input.text
  #   )
  #   return GQLBlogParagraph(
  #     id=blog_paragraph.id,
  #     text=blog_paragraph.text,
  #     index=blog_paragraph.index,
  #   )

  @strawberry.mutation
  @login_required
  def update_blog_paragraph(self, gql_input: BlogParagraphUpdateInput) -> GQLBlogParagraph:
    target_blog_paragraph = blog_service.update_blog_paragraph(
      uid=gql_input.id,
      title=gql_input.title,
      text=gql_input.text,
      index=gql_input.index
    )
    return to_gql_blog_paragraph(target_blog_paragraph)

  @strawberry.mutation
  @login_required
  def delete_blog_paragraph(self, uid: strawberry.ID) -> bool:
    blog_service.delete_blog_paragraph(uid)