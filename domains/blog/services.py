from typing import Optional, List, Dict
from cloudflare.index import CloudFlare
from .gql_types import BlogParagraphUpdateInput, BlogParagraphCreateInput
from .models import Blog, BlogParagraph
from extensions import db
from flask import Response, Blueprint, request, jsonify
import uuid

cf = CloudFlare()
blog_bp = Blueprint('blog', __name__, url_prefix='/api/blogs')


def reorder_blog_after_delete(target_blog):
  blogs = Blog.query.order_by('index').all()
  new_index = 0
  for b in blogs:
    if b.id == target_blog.id:
      continue
    else:
      b.index = new_index
      new_index += 1

def reorder_blog_after_delete_multiple(uids):
  blogs = Blog.query.order_by('index').all()
  new_index = 0
  for b in blogs:
    if b.id in uids:
      continue
    else:
      b.index = new_index
      new_index += 1


def list_blogs(limit, offset):
  return Blog.query.order_by(Blog.index).offset(offset).limit(limit).all()

def blog(uid) -> Optional[Blog]:
  return Blog.query.get(uid)

def count_blogs() -> int:
  return Blog.query.count()

@blog_bp.get('/image/<uid>/')
def retrieve_image(uid):
  paragraph_image = BlogParagraph.query.filter_by(image=uid).first()
  key = "noThumbnail.jpeg" if not paragraph_image else f'blogs/{uid}'
  obj = cf.get_object(key)
  body = obj['Body'].read()
  content_type = obj.get('ContentType', "image/jpeg")
  return Response(body, mimetype=content_type)

@blog_bp.post('/get-upload-url/<uid>')
def get_upload_url(uid):
  data = request.get_json(force=True) or {}
  filename = data.get('filename')
  folder = 'blogs'
  content_type = data.get('contentType') or "application/octet-stream"

  key = f'{folder}/{uid}'
  url = cf.generate_pre_signed_url(
    'put_object',
    key,
    filename
  )
  return jsonify({'uploadUrl': url, "key": key, "contentType": content_type})


def create_blog(title: str, subtitle: str, author: Optional[str], paragraphs: List[BlogParagraphCreateInput]) -> Optional[Blog]:
  new_blog = Blog(
    title=title,
    subtitle=subtitle,
    author=author,
    index=count_blogs(),
    paragraphs=[
      BlogParagraph(id=str(uuid.uuid4()), title=p.title, text=p.text, image=p.image, index=j)
      for j, p in enumerate(paragraphs or [])
    ],
  )
  db.session.add(new_blog)
  db.session.commit()
  return new_blog


def create_blog_paragraph(blog_id, title: str, text: str, image: str, index: int) -> Optional[BlogParagraph]:
  new_blog_paragraph = BlogParagraph(
    blog_id=blog_id,
    title=title,
    text=text,
    image=image,
    index=index
  )
  db.session.add(new_blog_paragraph)
  db.session.commit()
  return new_blog_paragraph

def update_blog(uid, title: Optional[str], subtitle: Optional[str], author: str, paragraphs: Optional[List[BlogParagraphUpdateInput]]) -> Optional[Blog]:
  target_blog = Blog.query.get(uid)
  if not target_blog:
    return None
  if title is not None:
    target_blog.title = title
  if subtitle is not None:
    target_blog.subtitle = subtitle
  if author is not None:
    target_blog.author = author

  for target_paragraph in paragraphs:
    if target_paragraph.id == '-1':
      create_blog_paragraph(target_blog.id, target_paragraph.title, target_paragraph.text, target_paragraph.image, target_paragraph.index)
    else:
      for paragraph in target_blog.paragraphs:
        if paragraph.id == target_paragraph.id:
          update_blog_paragraph(target_paragraph.id, target_paragraph.title, target_paragraph.text, target_paragraph.image, target_paragraph.index)
  db.session.commit()
  return target_blog

def update_blog_paragraph(uid, title: Optional[str], text: Optional[str], image: Optional[str], index: Optional[int]) -> Optional[BlogParagraph]:
  target_blog_paragraph = BlogParagraph.query.get(uid)
  if not target_blog_paragraph:
    return None
  if title is not None:
    target_blog_paragraph.title = title
  if text is not None:
    target_blog_paragraph.text = text
  if image is not None:
    target_blog_paragraph.image = image
  if index is not None:
    target_blog_paragraph.index = index
  db.session.commit()
  return target_blog_paragraph

def sort_blog(id_index_map: Dict[str, int]) -> bool:
  uids = list(id_index_map.keys())
  for uid in uids:
    b = Blog.query.get(uid)
    b.index = id_index_map.get(uid)
  db.session.commit()
  return True

def delete_blog(uid) -> Optional[List[Blog]]:
  target_blog = Blog.query.get(uid)
  for paragraph in target_blog.paragraphs:
    if paragraph.image:
      cf.delete_object(f"blogs/{paragraph.image}")
  db.session.delete(target_blog)
  reorder_blog_after_delete(target_blog)
  db.session.commit()
  return Blog.query.order_by('index').all()

def delete_blogs(uids: List[str]) -> List[Blog]:
  for uid in uids:
    target_blog = Blog.query.get(uid)
    if not target_blog:
      continue
    else:
      for paragraph in target_blog.paragraphs:
        if paragraph.image:
          cf.delete_object(f'blogs/{paragraph.image}')
      db.session.delete(target_blog)
  reorder_blog_after_delete_multiple(uids)
  db.session.commit()
  return Blog.query.order_by('index').all()

def delete_blog_paragraph(uid) -> bool:
  target_blog_paragraph = BlogParagraph.query.get(uid)
  if not target_blog_paragraph:
    return False
  db.session.delete(target_blog_paragraph)
  db.session.commit()
  return True
