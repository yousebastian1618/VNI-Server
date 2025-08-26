import strawberry
from typing import Optional, List
from .models import Blog, BlogImage, BlogParagraph

@strawberry.type
class GQLBlogImage:
  id: strawberry.ID
  url: str
  alt_text: Optional[str]
  order_index: int = 0

@strawberry.type
class GQLBlogParagraph:
  id: strawberry.ID
  text: str
  order_index: int = 0

@strawberry.type
class GQLBlog:
  id: strawberry.ID
  title: str
  subtitle: Optional[str]
  main_image: Optional[str]
  order_index: int = 0

  @strawberry.field
  def images(self) -> List[GQLBlogImage]:
    blog: Blog = Blog.query.get(self.id)
    return [
      GQLBlogImage(
        id=i.id,
        url=i.url,
        alt_text=i.alt_text,
        order_index=i.order_index
      ) for i in blog.images
    ]
  @strawberry.field
  def paragraphs(self) -> List[GQLBlogParagraph]:
    blog: Blog = Blog.query.get(self.id)
    return [
      GQLBlogParagraph(
        id=p.id,
        text=p.text,
        order_index=p.order_index
      ) for p in blog.paragraphs
    ]

@strawberry.input
class BlogImageInput:
  url: str
  alt_text: Optional[str]
  order_index: int = 0

@strawberry.input
class BlogParagraphInput:
  text: str
  order_index: int = 0

@strawberry.input
class BlogCreateInput:
  title: str
  subtitle: Optional[str] = None
  main_image: Optional[str] = None
  images: Optional[List[BlogImageInput]] = None
  paragraphs: Optional[List[BlogParagraphInput]] = None
  order_index: int = 0

@strawberry.input
class BlogUpdateInput:
  id: strawberry.ID
  title: Optional[str] = None
  subtitle: Optional[str] = None
  main_image: Optional[str] = None
  images: Optional[List[BlogImageInput]] = None
  paragraphs: Optional[List[BlogParagraphInput]] = None
  order_index: int = 0