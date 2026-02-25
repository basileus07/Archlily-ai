def estimate_infra_cost(storage_gb: float, cost_per_gb_per_month: float = 0.02):
    """
    Estimate yearly storage cost.
    Default: $0.02 per GB per month (S3-like pricing)
    """
    yearly_cost = storage_gb * cost_per_gb_per_month * 12
    return round(yearly_cost, 2)
