from typing import Optional, List
from helper.index import to_uuid
from .gql_types import BlogImageUpdateInput, BlogParagraphUpdateInput, BlogParagraphCreateInput
from .models import Blog, BlogImage, BlogParagraph
from extensions import db

def list_blogs(limit, offset):
  return Blog.query.order_by(Blog.index).offset(offset).limit(limit).all()

def blog(uid) -> Optional[Blog]:
  return Blog.query.get(to_uuid(uid))

def count_blogs() -> int:
  return Blog.query.count()

def create_blog(title: str, subtitle: str, images: List[str], paragraphs: List[BlogParagraphCreateInput]) -> Optional[Blog]:
  new_blog = Blog(
    title=title,
    subtitle=subtitle,
    index=count_blogs(),
  )
  db.session.add(new_blog)
  image_index = 0
  for _ in images:
    new_image = BlogImage(
      blog_id=new_blog.id,
      index=image_index
    )
    image_index += 1
    db.session.add(new_image)

  paragraph_index = 0
  for paragraph in paragraphs:
    new_paragraph = BlogParagraph(
      blog_id=new_blog.id,
      title=paragraph.title,
      text=paragraph.text,
      index=paragraph_index
    )
    paragraph_index += 1
    db.session.add(new_paragraph)
  db.session.commit()
  return new_blog

def create_blog_image(blog_id, index: int) -> List[BlogImage]:
  new_blog_image = BlogImage(
    blog_id=blog_id,
    index=index
  )
  db.session.add(new_blog_image)
  db.session.commit()
  return new_blog_image

def create_blog_paragraph(blog_id, title: str, text: str, index: int) -> Optional[BlogParagraph]:
  new_blog_paragraph = BlogParagraph(
    blog_id=blog_id,
    title=title,
    text=text,
    index=index
  )
  db.session.add(new_blog_paragraph)
  db.session.commit()
  return new_blog_paragraph

def update_blog(uid, title: Optional[str], subtitle: Optional[str], images: Optional[List[BlogImageUpdateInput]], paragraphs: Optional[List[BlogParagraphUpdateInput]]) -> Optional[Blog]:
  target_blog = Blog.query.get(to_uuid(uid))
  if not target_blog:
    return None
  if title is not None:
    target_blog.title = title
  if subtitle is not None:
    target_blog.subtitle = subtitle

  for target_image in images:
    for image in target_blog.images:
      if image.id == target_image.id:
        update_blog_image(target_image.id, target_image.index)
  for target_paragraph in paragraphs:
    for paragraph in target_blog.paragraphs:
      if paragraph.id == target_paragraph.id:
        update_blog_paragraph(target_paragraph.id, target_paragraph.title, target_paragraph.text, target_paragraph.index)
  db.session.commit()
  return target_blog

def update_blog_image(uid, index: Optional[int]) -> Optional[BlogImage]:
  target_blog_image = BlogImage.query.get(to_uuid(uid))
  if not target_blog_image:
    return None
  if index is not None:
    target_blog_image.index = index
  db.session.commit()
  return target_blog_image

def update_blog_paragraph(uid, title: Optional[str], text: Optional[str], index: Optional[int]) -> Optional[BlogParagraph]:
  target_blog_paragraph = BlogParagraph.query.get(to_uuid(uid))
  if not target_blog_paragraph:
    return None
  if title is not None:
    target_blog_paragraph.title = title
  if text is not None:
    target_blog_paragraph.text = text
  if index is not None:
    target_blog_paragraph.index = index
  db.session.commit()
  return target_blog_paragraph

def delete_blog(uid) -> bool:
  target_blog = Blog.query.get(to_uuid(uid))
  if not target_blog:
    return False
  db.session.delete(target_blog)
  db.session.commit()
  return True

def delete_blog_image(uid) -> bool:
  target_blog_image = BlogImage.query.get(to_uuid(uid))
  if not target_blog_image:
    return False
  db.session.delete(target_blog_image)
  db.session.commit()
  return True

def delete_blog_paragraph(uid) -> bool:
  target_blog_paragraph = BlogParagraph.query.get(to_uuid(uid))
  if not target_blog_paragraph:
    return False
  db.session.delete(target_blog_paragraph)
  db.session.commit()
  return True
