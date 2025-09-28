from domains.maintenance.models import Maintenance
from extensions import db

def get_maintenance() -> Maintenance:
  current_maintenance = Maintenance.query.all()[0]
  return current_maintenance

def toggle_maintenance(toggle: bool) -> Maintenance:
  current_maintenance = Maintenance.query.all()[0]
  current_maintenance.maintenance = toggle
  db.session.commit()
  return current_maintenance
