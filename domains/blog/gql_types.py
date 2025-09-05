import strawberry
from typing import Optional, List
from .models import Blog

@strawberry.type
class GQLBlogImage:
  id: str
  index: int = 0

@strawberry.type
class GQLBlogParagraph:
  id: str
  title: str
  text: str
  index: int = 0

@strawberry.type
class GQLBlog:
  id: strawberry.ID
  title: str
  subtitle: Optional[str]
  author: Optional[str]
  index: int = 0

  @strawberry.field
  def images(self) -> List[GQLBlogImage]:
    blog: Blog = Blog.query.get(self.id)
    return [
      GQLBlogImage(
        id=i.id,
        index=i.index
      ) for i in blog.images
    ]
  @strawberry.field
  def paragraphs(self) -> List[GQLBlogParagraph]:
    blog: Blog = Blog.query.get(self.id)
    return [
      GQLBlogParagraph(
        id=p.id,
        title=p.title,
        text=p.text,
        index=p.index
      ) for p in blog.paragraphs
    ]

@strawberry.input
class BlogParagraphCreateInput:
  title: str
  text: str

@strawberry.input
class BlogImageUpdateInput:
  id: strawberry.ID
  index: int

@strawberry.input
class BlogParagraphUpdateInput:
  id: strawberry.ID
  title: str
  text: str
  index: int

@strawberry.input
class BlogCreateInput:
  title: str
  subtitle: Optional[str] = None
  author: Optional[str] = None
  images: Optional[List[int]] = None
  paragraphs: Optional[List[BlogParagraphCreateInput]] = None
  index: int = 0

@strawberry.input
class BlogUpdateInput:
  id: strawberry.ID
  title: Optional[str] = None
  subtitle: Optional[str] = None
  author: Optional[str] = None
  images: Optional[List[BlogImageUpdateInput]] = None
  paragraphs: Optional[List[BlogParagraphUpdateInput]] = None
  index: int = 0