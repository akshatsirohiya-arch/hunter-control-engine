# engine/metrics.py
# Market damage metrics (binary: 0 or 1)

def index_trend_damage(index_df):
    """
    Returns 1 if index is below 50-DMA and fails to reclaim.
    """
    recent = index_df.tail(15)
    below_50 = recent["Close"] < recent["DMA_50"]

    if below_50.any():
        reclaimed = recent["Close"].iloc[-1] > recent["DMA_50"].iloc[-1]
        if not reclaimed:
            return 1
    return 0


def major_trend_failure(index_df):
    """
    Returns 1 if index stays below 200-DMA for 5 consecutive days.
    """
    recent = index_df.tail(5)
    if (recent["Close"] < recent["DMA_200"]).all():
        return 1
    return 0


def breadth_collapse(breadth_percent):
    """
    Returns 1 if breadth is below 40%.
    """
    if breadth_percent < 40:
        return 1
    return 0


def volatility_instability(vix_change_pct):
    """
    Returns 1 if VIX expands more than 30% in 5 days.
    """
    if vix_change_pct >= 0.30:
        return 1
    return 0
