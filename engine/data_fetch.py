# engine/data_fetch.py
# Responsible for fetching and sanitizing market data

import yfinance as yf
import pandas as pd


def fetch_price_data(ticker, lookback_days=300):
    """
    Fetches historical price data and guarantees:
    - Close is a 1D float Series
    - No multi-index columns
    - Clean numeric data
    """
    df = yf.download(
        ticker,
        period=f"{lookback_days}d",
        auto_adjust=True,
        progress=False
    )

    # Drop empty rows
    df = df.dropna(how="all")

    # If columns are multi-index, flatten them
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Force Close to be a clean Series
    close = df["Close"]
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]

    df = pd.DataFrame({
        "Close": close.astype(float)
    }, index=df.index)

    return df


def add_moving_averages(df):
    """
    Adds 50-DMA and 200-DMA safely.
    """
    df = df.copy()
    df["DMA_50"] = df["Close"].rolling(50).mean()
    df["DMA_200"] = df["Close"].rolling(200).mean()
    return df


def get_vix_change_pct():
    """
    Returns VIX percentage change over last 5 trading days.
    """
    df = fetch_price_data("^VIX", lookback_days=10)

    if len(df) < 6:
        return 0.0

    start = float(df["Close"].iloc[-6])
    end = float(df["Close"].iloc[-1])

    return (end - start) / start


def get_breadth_percent():
    """
    Simple breadth proxy using SPY and QQQ.
    """
    tickers = ["SPY", "QQQ"]
    above = 0

    for ticker in tickers:
        df = add_moving_averages(fetch_price_data(ticker))

        close = float(df["Close"].iloc[-1])
        dma_50 = float(df["DMA_50"].iloc[-1])

        if close > dma_50:
            above += 1

    return (above / len(tickers)) * 100
