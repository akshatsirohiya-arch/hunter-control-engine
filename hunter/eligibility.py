# hunter/eligibility.py
# Determines if a stock is eligible for hunting (moderate mode)

from engine.data_fetch import fetch_price_data, add_moving_averages
import numpy as np


def is_eligible(stock_df, index_df):
    """
    Returns True if stock passes moderate hunter eligibility rules.
    Robust to missing / bad data.
    """

    # Ensure enough data
    if len(stock_df) < 200 or len(index_df) < 200:
        return False

    stock = add_moving_averages(stock_df)
    index = index_df.copy()

    # Drop rows with missing values
    stock = stock.dropna()
    index = index.dropna()

    if len(stock) < 200 or len(index) < 200:
        return False

    # --- Gate 1: Structure ---
    close = float(stock["Close"].iloc[-1])
    dma_50 = float(stock["DMA_50"].iloc[-1])
    dma_200 = float(stock["DMA_200"].iloc[-1])

    if close < dma_50 or close < dma_200:
        return False

    # --- Gate 2: Relative survival (60 days) ---
    stock_60 = stock["Close"].iloc[-60:]
    index_60 = index["Close"].iloc[-60:]

    if stock_60.isnull().any() or index_60.isnull().any():
        return False

    stock_return = (stock_60.iloc[-1] - stock_60.iloc[0]) / stock_60.iloc[0]
    index_return = (index_60.iloc[-1] - index_60.iloc[0]) / index_60.iloc[0]

    if not (stock_return > index_return or (index_return < 0 and stock_return >= 0)):
        return False

    # --- Gate 3: Behavior ---
    recent = stock["Close"].iloc[-15:]

    if recent.isnull().any():
        return False

    range_pct = (recent.max() - recent.min()) / recent.min()

    high_60 = stock["Close"].iloc[-60:].max()
    pullback = (high_60 - close) / high_60

    behavior_ok = (
        range_pct <= 0.12 or
        pullback <= 0.15
    )

    # Extension check
    extension = (close - dma_50) / dma_50
    if extension > 0.40:
        return False

    return behavior_ok
