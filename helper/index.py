from uuid import UUID
from flask import request

def to_uuid(value):
  if value is None:
    return None
  if isinstance(value, UUID):
    return value
  return UUID(str(value))

def get_client_ip() -> str:
  # Cloudflare (if you use it)
  ip = request.headers.get("CF-Connecting-IP")
  if ip:
    return ip

  # Some CDNs/WAFs (Akamai/Fastly)
  ip = request.headers.get("True-Client-IP")
  if ip:
    return ip

  # Standard proxy chain (ALB/CloudFront/Nginx/etc.)
  xff = request.headers.get("X-Forwarded-For", "")
  if xff:
    # left-most is the original client
    return xff.split(",")[0].strip()

  # Direct connection fallback
  return request.remote_addr