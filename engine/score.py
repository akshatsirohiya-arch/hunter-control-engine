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
    spx = add_moving_averages(fetch_price_data(spx_ticker))
    ndx = add_moving_averages(fetch_price_data(ndx_ticker))

    metrics = {}

    metrics["Index below 50-DMA (reclaim failed)"] = max(
        index_trend_damage_v2(spx),
        index_trend_damage_v2(ndx)
    )

    metrics["Index below 200-DMA"] = max(
        major_trend_failure_v2(spx),
        major_trend_failure_v2(ndx)
    )

    metrics["Breadth < 40%"] = breadth_collapse(breadth_percent)

    metrics["Volatility expansion (VIX)"] = volatility_instability(vix_change_pct)

    damage_score = sum(metrics.values())

    return damage_score, metrics
