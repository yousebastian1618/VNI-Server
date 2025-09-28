from domains.maintenance.gql_types import GQLMaintenance, ToggleMaintenanceInput
from . import services as maintenance_service
import strawberry

def to_gql_maintenance(m) -> GQLMaintenance:
  return GQLMaintenance(
    id=m.id,
    maintenance=m.maintenance
  )

@strawberry.type
class MaintenanceMutation:
  @strawberry.mutation
  def toggle_maintenance(self, gql_input: ToggleMaintenanceInput) -> GQLMaintenance:
    current_maintenance = maintenance_service.toggle_maintenance(toggle=gql_input.maintenance)
    return to_gql_maintenance(current_maintenance)
