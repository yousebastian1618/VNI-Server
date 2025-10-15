from typing import List, Optional
from extensions import db
from .models import Product
from cloudflare.index import CloudFlare
from flask import Blueprint, Response, request, jsonify

cf = CloudFlare()
product_bp = Blueprint("product", __name__, url_prefix="/api/products")

def reorder_products_after_delete(deleting_product: Product):
  products = Product.query.order_by('index').all()
  new_index = 0
  for product in products:
    if product.id == deleting_product.id:
      continue
    else:
      product.index = new_index
      new_index += 1

def reorder_products_after_delete_multiple(uids: List[str]):
  products = Product.query.order_by('index').all()
  new_index = 0
  for product in products:
    if product.id in uids:
      continue
    else:
      product.index = new_index
      new_index += 1

def list_products() -> List[Product]:
  return Product.query.order_by('index').all()

def get_product(uid) -> Optional[Product]:
  return Product.query.get(uid)

def count_products() -> int:
  return Product.query.count()

def create_product() -> Product:
  product = Product(
    index=count_products(),
  )
  db.session.add(product)
  db.session.commit()
  return product

@product_bp.get("/image/<uid>/")
def retrieve_image(uid):
  product = Product.query.get(uid)
  key = "noThumbnail.jpeg" if not product else f'products/{uid}'
  obj = cf.get_object(key)
  body = obj['Body'].read()
  content_type = obj.get("ContentType", "image/jpeg")
  return Response(body, mimetype=content_type)

@product_bp.post('/get-upload-url/<uuid>/')
def get_upload_url(uuid):
  data = request.get_json(force=True) or {}
  filename = data.get('filename')
  folder = 'products'
  content_type = data.get('contentType') or "application/octet-stream"

  key = f'{folder}/{uuid}'
  url = cf.generate_pre_signed_url(
    "put_object",
    key,
    filename
  )
  return jsonify({'uploadUrl': url, "key": key, "contentType": content_type})


def update_product(uid, index: Optional[int]=None) -> Optional[Product]:
  product = Product.query.get(uid)
  if not product:
      return None
  if index is not None: product.index = index
  db.session.commit()
  return product

def reorder_products(product_index_map) -> bool:
  for item in product_index_map:
    pid = getattr(item, 'id')
    idx = getattr(item, 'index')
    idx = int(idx)
    product = db.session.get(Product, pid)
    if product is None:
      raise ValueError(f"Unknown product id: {pid}")
    product.index = idx
  db.session.commit()
  return True

def delete_product(uid) -> bool:
  product = Product.query.get(uid)
  if not product:
      return False
  reorder_products_after_delete(product)
  db.session.delete(product)
  db.session.commit()
  return True

def delete_products(uids: List[str]) -> List[Product]:
  for uid in uids:
    product = Product.query.get(uid)
    if not product:
      continue
    else:
      cf.delete_object(f'products/{uid}')
      db.session.delete(product)
  reorder_products_after_delete_multiple(uids)
  db.session.commit()
  return Product.query.order_by('index').all()