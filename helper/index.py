from uuid import UUID

def to_uuid(value):
  if value is None:
    return None
  if isinstance(value, UUID):
    return value
  return UUID(str(value))