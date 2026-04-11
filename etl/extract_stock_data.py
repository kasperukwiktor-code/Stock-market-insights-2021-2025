import yfinance as yf
import pandas as pd
from datetime import datetime

TICKERS = ["TSLA", "AAPL", "MSFT", "PLTR", "AMD", "LMT", "AVGO"]

START_DATE = "2021-01-01"
END_DATE = "2025-01-01"

def extract_data(ticker):
    df = yf.download(ticker, start=START_DATE, end=END_DATE)
    df.columns = df.columns.get_level_values(0)  # ← spłaszcza MultiIndex
    df.reset_index(inplace=True)
    df["ticker"] = ticker
    return df


def transform_data(df):
    if df.empty:
        print("Warning: empty dataframe")
        return df
    df = df.dropna()
    df.columns = [col.lower() for col in df.columns]
    df["daily_return"] = df["close"].pct_change()
    df["moving_avg_7d"] = df["close"].rolling(window=7).mean()
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    return df


def load_data(df, ticker):
    today = datetime.today().strftime("%Y-%m-%d")
    file_name = f"data/{ticker}_{today}.csv"
    df.to_csv(file_name, index=False)


def run_pipeline():
    all_data = []

    for ticker in TICKERS:
        print(f"Processing {ticker}...")
        df = extract_data(ticker)
        df = transform_data(df)
        load_data(df, ticker)
        all_data.append(df)

    final_df = pd.concat(all_data)
    final_df.to_csv("data/all_stocks.csv", index=False)


if __name__ == "__main__":
    run_pipeline()