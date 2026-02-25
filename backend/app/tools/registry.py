from app.tools.storage_estimator import estimate_storage
from app.tools.cost_estimator import estimate_infra_cost
from app.tools.qps_estimator import estimate_qps

# central tool registry
TOOL_REGISTRY = {
    "estimate_storage": estimate_storage,
    "estimate_qps": estimate_qps,
    "estimate_infra_cost": estimate_infra_cost,
}
