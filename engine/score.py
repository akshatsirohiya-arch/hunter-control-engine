# engine/score.py
# Computes overall market damage score

from engine.data_fetch import fetch_price_data, add_moving_averages
from engine.metrics import (
    index_trend_damage_v2,
    major_trend_failure_v2,
    breadth_collapse,
    volatility_instability
)


def compute_damage_score(
    spx_ticker="^GSPC",
    ndx_ticker="^IXIC",
    breadth_percent=50,
    vix_change_pct=0.0
):
    """
    Returns damage score from 0 to 6.
    """

    # Fetch index data
    spx = add_moving_averages(fetch_price_data(spx_ticker))
    ndx = add_moving_averages(fetch_price_data(ndx_ticker))

    score = 0

    # Metric 1: Index trend damage
    score += max(
        index_trend_damage_v2(spx),
index_trend_damage_v2(ndx)

    )

    # Metric 2: Major trend failure
    score += max(
        major_trend_failure_v2(spx),
major_trend_failure_v2(ndx)

    )

    # Metric 3: Breadth collapse
    score += breadth_collapse(breadth_percent)

    # Metric 4: Volatility instability
    score += volatility_instability(vix_change_pct)

    return score
