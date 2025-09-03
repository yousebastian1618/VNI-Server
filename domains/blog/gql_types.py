import strawberry
from typing import Optional, List
from .models import Blog

@strawberry.type
class GQLBlogImage:
  id: strawberry.ID
  index: int = 0

@strawberry.type
class GQLBlogParagraph:
  id: strawberry.ID
  title: str
  text: str
  index: int = 0

@strawberry.type
class GQLBlog:
  id: strawberry.ID
  title: str
  subtitle: Optional[str]
  index: int = 0
  images: List[GQLBlogImage] = []
  paragraphs: List[GQLBlogParagraph] = []

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

@strawberry.type
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
  images: Optional[List[str]] = None
  paragraphs: Optional[List[str]] = None
  index: int = 0

@strawberry.input
class BlogUpdateInput:
  id: strawberry.ID
  title: Optional[str] = None
  subtitle: Optional[str] = None
  images: Optional[List[BlogImageUpdateInput]] = None
  paragraphs: Optional[List[BlogParagraphUpdateInput]] = None
  index: int = 0