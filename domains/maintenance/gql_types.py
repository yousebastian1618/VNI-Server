import strawberry


@strawberry.type
class GQLMaintenance:
  id: str
  maintenance: bool

@strawberry.input
class ToggleMaintenanceInput:
  maintenance: bool
