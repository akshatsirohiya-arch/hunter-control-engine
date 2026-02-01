# engine/data_fetch.py
# Responsible for fetching market data

import yfinance as yf
import pandas as pd


def fetch_price_data(ticker, lookback_days=300):
    """
    Fetches historical price data for a ticker.
    """
    df = yf.download(
        ticker,
        period=f"{lookback_days}d",
        auto_adjust=True,
        progress=False
    )

    df = df.dropna()
    return df


def add_moving_averages(df):
    """
    Adds 50-DMA and 200-DMA to price dataframe.
    """
    df["DMA_50"] = df["Close"].rolling(50).mean()
    df["DMA_200"] = df["Close"].rolling(200).mean()
    return df

def get_vix_change_pct():
    """
    Returns VIX percentage change over last 5 trading days.
    """
    df = yf.download(
        "^VIX",
        period="10d",
        auto_adjust=True,
        progress=False
    ).dropna()

    if len(df) < 6:
        return 0.0

    start = df["Close"].iloc[-6]
    end = df["Close"].iloc[-1]

    return (end - start) / start


def get_breadth_percent():
    """
    Simple breadth proxy using SPY and QQQ.
    Returns percentage above 50-DMA.
    """
    tickers = ["SPY", "QQQ"]
    above = 0

    for ticker in tickers:
        df = fetch_price_data(ticker)
        df = add_moving_averages(df)

        close_price = float(df["Close"].iloc[-1])
        dma_50 = float(df["DMA_50"].iloc[-1])

        if close_price > dma_50:
            above += 1

    return (above / len(tickers)) * 100

