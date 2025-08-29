import strawberry
from typing import Optional, List
from .models import Blog, BlogImage, BlogParagraph

@strawberry.type
class GQLBlogImage:
  id: strawberry.ID
  url: str
  alt_text: Optional[str]
  index: int = 0

@strawberry.type
class GQLBlogParagraph:
  id: strawberry.ID
  text: str
  index: int = 0

@strawberry.type
class GQLBlog:
  id: strawberry.ID
  title: str
  subtitle: Optional[str]
  main_image: Optional[str]
  index: int = 0

  @strawberry.field
  def images(self) -> List[GQLBlogImage]:
    blog: Blog = Blog.query.get(self.id)
    return [
      GQLBlogImage(
        id=i.id,
        url=i.url,
        alt_text=i.alt_text,
        index=i.index
      ) for i in blog.images
    ]
  @strawberry.field
  def paragraphs(self) -> List[GQLBlogParagraph]:
    blog: Blog = Blog.query.get(self.id)
    return [
      GQLBlogParagraph(
        id=p.id,
        text=p.text,
        index=p.index
      ) for p in blog.paragraphs
    ]

@strawberry.input
class BlogImageInput:
  url: str
  alt_text: Optional[str]
  index: int = 0

@strawberry.input
class BlogParagraphInput:
  text: str
  index: int = 0

@strawberry.input
class BlogCreateInput:
  title: str
  subtitle: Optional[str] = None
  main_image: Optional[str] = None
  images: Optional[List[BlogImageInput]] = None
  paragraphs: Optional[List[BlogParagraphInput]] = None
  index: int = 0

@strawberry.input
class BlogUpdateInput:
  id: strawberry.ID
  title: Optional[str] = None
  subtitle: Optional[str] = None
  main_image: Optional[str] = None
  images: Optional[List[BlogImageInput]] = None
  paragraphs: Optional[List[BlogParagraphInput]] = None
  index: int = 0