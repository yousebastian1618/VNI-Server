import strawberry
from auth.guard import login_required
from .gql_types import GQLBlog, BlogCreateInput, BlogUpdateInput, GQLBlogParagraph, BlogParagraphUpdateInput, BlogParagraphCreateInput
from typing import Optional, List
from . import services as blog_service





#BLOG PARAGRAPH MUTATIONS
def to_gql_blog_paragraph(blog_paragraph) -> GQLBlogParagraph:
  return GQLBlogParagraph(
    id=blog_paragraph.id,
    title=blog_paragraph.title,
    text=blog_paragraph.text,
    image=blog_paragraph.image,
    index=blog_paragraph.index,
  )

class ParagraphMutation:
  @strawberry.mutation
  def create_blog_paragraph(self, gql_input: BlogParagraphCreateInput) -> GQLBlogParagraph:
    blog_paragraph = blog_service.create_blog_paragraph(
      gql_input.text
    )
    return GQLBlogParagraph(
      id=blog_paragraph.id,
      text=blog_paragraph.text,
      image=blog_paragraph.image,
      index=blog_paragraph.index,
    )

  @strawberry.mutation
  # @login_required
  def update_blog_paragraph(self, gql_input: BlogParagraphUpdateInput) -> GQLBlogParagraph:
    target_blog_paragraph = blog_service.update_blog_paragraph(
      uid=gql_input.id,
      title=gql_input.title,
      text=gql_input.text,
      image=gql_input.image,
      index=gql_input.index
    )
    return to_gql_blog_paragraph(target_blog_paragraph)

  @strawberry.mutation
  # @login_required
  def delete_blog_paragraph(self, uid: strawberry.ID) -> bool:
    return blog_service.delete_blog_paragraph(uid)












# BLOG MUTATIONS
def to_gql_blog(blog) -> GQLBlog:
  return GQLBlog(
    id=blog.id,
    title=blog.title,
    subtitle=blog.subtitle,
    author=blog.author,
    index=blog.index,
  )

@strawberry.type
class BlogMutations:
  @strawberry.mutation
  # @login_required
  def create_blog(self, gql_input: BlogCreateInput) -> GQLBlog:
    blog = blog_service.create_blog(
      title=gql_input.title,
      subtitle=gql_input.subtitle,
      author=gql_input.author,
      paragraphs=gql_input.paragraphs
    )
    return to_gql_blog(blog)

  @strawberry.mutation
  # @login_required
  def update_blog(self, gql_input: BlogUpdateInput) -> Optional[GQLBlog]:
    target_blog = blog_service.update_blog(
      uid=gql_input.id,
      title=gql_input.title,
      subtitle=gql_input.subtitle,
      author=gql_input.author,
      paragraphs=gql_input.paragraphs
    )
    return to_gql_blog(target_blog)

  @strawberry.mutation
  def reorder_blogs(self, gql_input: List[BlogUpdateInput]) -> bool:
    id_index_map: dict[str, int] = {
      str(item.id): int(item.index)  # ensure types
      for item in gql_input
      if item.index is not None
    }
    return blog_service.sort_blog(id_index_map)

  @strawberry.mutation
  # @login_required
  def delete_blog(self, uid: strawberry.ID) -> bool:
    return blog_service.delete_blog(uid)

  @strawberry.mutation
  # @login_required
  def delete_blogs(self, uids: List[str]) -> List[GQLBlog]:
    items = blog_service.delete_blogs(uids)
    return [to_gql_blog(b) for b in items];