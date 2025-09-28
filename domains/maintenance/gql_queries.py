from domains.maintenance.gql_types import GQLMaintenance
import strawberry
from . import services as maintenance_service


def to_gql_maintenance(m) -> GQLMaintenance:
  return GQLMaintenance(
    id=m.id,
    maintenance=m.maintenance
  )

@strawberry.type
class MaintenanceQueries:
  @strawberry.field
  def maintenance(self) -> GQLMaintenance:
    current_maintenance = maintenance_service.get_maintenance()
    return to_gql_maintenance(current_maintenance)
