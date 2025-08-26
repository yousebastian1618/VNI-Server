import strawberry
from datetime import datetime

@strawberry.type
class GQLInquiry:
  id: strawberry.ID
  first_name: str
  last_name: str
  email: str
  subject: str
  text: str
  sent_at: datetime
  resolved: bool

@strawberry.input
class InquiryCreateInput:
  first_name: str
  last_name: str
  email: str
  subject: str
  text: str

