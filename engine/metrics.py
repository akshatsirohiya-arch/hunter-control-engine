# engine/metrics.py
# Market damage metrics (binary: 0 or 1)

def index_trend_damage_v2(index_df):
    recent = index_df.tail(15)

    close_vals = recent["Close"].astype(float).values
    dma_vals = recent["DMA_50"].astype(float).values

    below_50 = close_vals < dma_vals

    if below_50.any() and close_vals[-1] <= dma_vals[-1]:
        return 1
    return 0


def major_trend_failure_v2(index_df):
    recent = index_df.tail(5)

    close_vals = recent["Close"].astype(float).values
    dma_vals = recent["DMA_200"].astype(float).values

    if (close_vals < dma_vals).all():
        return 1
    return 0


def breadth_collapse(breadth_percent):
    return 1 if breadth_percent < 40 else 0


def volatility_instability(vix_change_pct):
    vix_val = float(vix_change_pct)
    return 1 if vix_val >= 0.30 else 0

