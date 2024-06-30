import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import cryptocompare


def run():
    # Fetch Bitcoin data from CryptoCompare
    df = cryptocompare.get_historical_price_day('BTC', currency='USD', limit=500, toTs=pd.Timestamp.today())
    df = pd.DataFrame(df)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True, drop=False)

    # Calculate EMA21 and SMA50
    df['EMA21'] = df['close'].ewm(span=21, adjust=False).mean()
    df['SMA50'] = df['close'].rolling(window=50).mean()

    plt.style.use ('seaborn-v0_8-paper')
    fig, ax = plt.subplots(figsize=(14, 8))

    # Plot closing price, EMA21 and SMA50
    ax.plot(df.index, df['close'], label='Bitcoin Close Price', linewidth=0.55)
    ax.plot(df.index, df['EMA21'], label='21 Day EMA', linewidth=0.85)
    ax.plot(df.index, df['SMA50'], label='50 Day SMA', linewidth=0.85)

    # Set the title and labels
    ax.set_title('Bitcoin Close Prices with EMA21 and SMA50')
    ax.set_ylabel('Price (USD)')

    # Improve date formatting
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # Display only year and month

    plt.xticks(rotation=45)
    plt.tick_params(axis='x', labelsize=8)

    # Add a legend
    ax.legend()

    # Save the figure
    plt.savefig('bitcoin_ema21_sma50.png')

    # Show the plot
    plt.show()


if __name__ == '__main__':
    run()
