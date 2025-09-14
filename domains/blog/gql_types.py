import strawberry
from typing import Optional, List
from .models import Blog

# BLOG PARAGRAPH
@strawberry.type
class GQLBlogParagraph:
  id: str
  title: Optional[str]
  text: Optional[str]
  image: Optional[str]
  index: int = 0

@strawberry.input
class BlogParagraphCreateInput:
  title: Optional[str]
  text: Optional[str]
  image: Optional[str]

@strawberry.input
class BlogParagraphUpdateInput:
  id: strawberry.ID
  title: Optional[str]
  text: Optional[str]
  image: Optional[str]
  index: int





# BLOG
@strawberry.type
class GQLBlog:
  id: strawberry.ID
  title: str
  subtitle: Optional[str]
  author: Optional[str]
  index: int = 0


  @strawberry.field
  def paragraphs(self) -> List[GQLBlogParagraph]:
    blog: Blog = Blog.query.get(self.id)
    return [
      GQLBlogParagraph(
        id=p.id,
        title=p.title,
        text=p.text,
        image=p.image,
        index=p.index
      ) for p in blog.paragraphs
    ]



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
  paragraphs: Optional[List[BlogParagraphUpdateInput]] = None
  index: Optional[int] = 0