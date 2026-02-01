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
