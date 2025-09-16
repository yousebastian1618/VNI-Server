import logging
import boto3
from botocore.exceptions import ClientError
from botocore.client import Config
from flask import current_app
import os


class CloudFlare:
  def __init__(self):
    self.s3_client = boto3.client(
      's3',
      endpoint_url=f"https://{os.environ.get('CLOUDFLARE_ACCOUNT_ID')}.r2.cloudflarestorage.com",
      aws_access_key_id=os.environ.get('CLOUDFLARE_ACCESS_KEY_ID'),
      aws_secret_access_key=os.environ.get('CLOUDFLARE_SECRET_ACCESS_KEY'),
      region_name='auto',
      config = Config(signature_version="s3v4"),
    )

  def list_objects(self, key):
    return self.s3_client.list_objects_v2(
      Bucket=current_app.config.get('BUCKET'),
      Delimiter='/',
      Prefix=key
    )

  def get_object(self, key):
    try:
      return self.s3_client.get_object(
        Bucket=current_app.config.get('BUCKET'),
        Key=key
      )
    except ClientError as e:
      logging.error(e)
      return False

  def post_object(self, file, name):
    try:
      response = self.s3_client.upload_fileobj(
        Fileobj=file,
        Bucket=current_app.config.get('BUCKET'),
        Key=name
      )
    except ClientError as e:
      logging.error(e)
      return None
    return response

  def delete_object(self, key):
    try:
      response = self.s3_client.delete_object(
        Bucket=current_app.config.get('BUCKET'),
        Key=key
      )
    except ClientError as e:
      logging.error(e)
      return None
    return response

  def generate_pre_signed_url(self, method, key, name):
    try:
      response = self.s3_client.generate_presigned_url(
        method,
        Params={
          'Bucket': current_app.config.get('BUCKET'),
          'Key': key,
        },
        ExpiresIn=3600
      )
    except ClientError as e:
      logging.error(e)
      return None
    return response