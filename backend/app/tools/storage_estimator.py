def estimate_storage(
    events_per_day: int,
    avg_event_size_kb: float = 2.0,
    retention_days: int = 365,
):
    """
    Generic storage estimator.
    Defaults:
    - avg_event_size_kb = 2 KB
    - retention_days = 365 days
    """

    total_events = events_per_day * retention_days
    total_kb = total_events * avg_event_size_kb
    total_gb = total_kb / (1024 * 1024)

    return round(total_gb, 2)