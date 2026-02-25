def estimate_qps(events_per_day: int):
    """
    Estimate average and peak QPS.
    Assumes:
    - Traffic not uniform
    - Peak = 3x average
    """
    seconds_per_day = 86400
    avg_qps = events_per_day / seconds_per_day
    peak_qps = avg_qps * 3

    return {
        "average_qps": round(avg_qps, 2),
        "peak_qps": round(peak_qps, 2),
    }