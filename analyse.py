import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.subplots as sp
import base64
from io import BytesIO
from datetime import datetime, timedelta

def fetch_stock_data(symbol):
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')
    stock_data = yf.download(symbol, start=start_date, end=end_date)
    return stock_data

def calculate_macd(df, short_window=12, long_window=26, signal_window=9):
    df['ema_short'] = df['Close'].ewm(span=short_window, adjust=False).mean()
    df['ema_long'] = df['Close'].ewm(span=long_window, adjust=False).mean()
    df['macd'] = df['ema_short'] - df['ema_long']
    df['signal_line'] = df['macd'].ewm(span=signal_window, adjust=False).mean()
    df['macd_signal'] = np.where(df['macd'] > df['signal_line'], 'Al', 'Sat')
    return df

def calculate_rsi(df, window=14):
    delta = df['Close'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()

    rs = avg_gain / avg_loss
    df['rsi'] = 100 - (100 / (1 + rs))
    df['rsi_signal'] = np.where(df['rsi'] < 30, 'Al', np.where(df['rsi'] > 70, 'Sat', 'Tut'))
    return df

def calculate_bollinger_bands(df, window=20, num_std_dev=2):
    df['rolling_mean'] = df['Close'].rolling(window).mean()
    df['rolling_std'] = df['Close'].rolling(window).std()
    df['upper_band'] = df['rolling_mean'] + (df['rolling_std'] * num_std_dev)
    df['lower_band'] = df['rolling_mean'] - (df['rolling_std'] * num_std_dev)
    df['bb_signal'] = np.where(df['Close'] < df['lower_band'], 'Al', np.where(df['Close'] > df['upper_band'], 'Sat', 'Tut'))
    return df

def get_price_change_graph(stock_symbol):
    stock = yf.Ticker(stock_symbol)
    hist = stock.history(period="1y")

    # Fiyat değişimlerini hesapla
    hist['PriceChange'] = hist['Close'].pct_change() * 100

    # %5'ten fazla değişim olan noktaları belirle
    breakpoints = hist[abs(hist['PriceChange']) > 5]

    # MACD Hesapla
    hist = calculate_macd(hist)

    # RSI Hesapla
    hist = calculate_rsi(hist)

    # Bollinger Bands Hesapla
    hist = calculate_bollinger_bands(hist)

    fig = sp.make_subplots(rows=3, cols=1, shared_xaxes=True,
                           vertical_spacing=0.02,
                           row_heights=[0.5, 0.25, 0.25])

    # Add Candlestick chart with Bollinger Bands
    fig.add_trace(go.Candlestick(x=hist.index,
                                 open=hist['Open'],
                                 high=hist['High'],
                                 low=hist['Low'],
                                 close=hist['Close'],
                                 name='Candlestick'),
                  row=1, col=1)

    # Add line chart for close prices
    fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], mode='lines', name='Close', line=dict(color='blue')),
                  row=1, col=1)

    fig.add_trace(go.Scatter(x=hist.index, y=hist['upper_band'], mode='lines', name='Upper Band', line=dict(color='green')), row=1, col=1)
    fig.add_trace(go.Scatter(x=hist.index, y=hist['lower_band'], mode='lines', name='Lower Band', line=dict(color='red')), row=1, col=1)
    fig.add_trace(go.Scatter(x=hist.index, y=hist['upper_band'], mode='lines', line=dict(width=0), showlegend=False), row=1, col=1)
    fig.add_trace(go.Scatter(x=hist.index, y=hist['lower_band'], mode='lines', fill='tonexty', fillcolor='rgba(0, 100, 80, 0.2)', line=dict(width=0), showlegend=False), row=1, col=1)

    # Add MACD
    fig.add_trace(go.Scatter(x=hist.index, y=hist['macd'], mode='lines', name='MACD', line=dict(color='blue')), row=2, col=1)
    fig.add_trace(go.Scatter(x=hist.index, y=hist['signal_line'], mode='lines', name='Signal Line', line=dict(color='red')), row=2, col=1)

    # MACD Al/Sat sinyalleri ekle
    for i in range(1, len(hist)):
        if hist['macd_signal'].iloc[i] == 'Al' and hist['macd_signal'].iloc[i-1] == 'Sat':
            fig.add_annotation(
                x=hist.index[i],
                y=hist['macd'].iloc[i],
                text='Al',
                showarrow=True,
                arrowhead=1,
                ax=0,
                ay=-30,
                font=dict(color='green'),
                row=2, col=1
            )
        elif hist['macd_signal'].iloc[i] == 'Sat' and hist['macd_signal'].iloc[i-1] == 'Al':
            fig.add_annotation(
                x=hist.index[i],
                y=hist['macd'].iloc[i],
                text='Sat',
                showarrow=True,
                arrowhead=1,
                ax=0,
                ay=30,
                font=dict(color='red'),
                row=2, col=1
            )

    # Add RSI
    fig.add_trace(go.Scatter(x=hist.index, y=hist['rsi'], mode='lines', name='RSI', line=dict(color='purple')), row=3, col=1)
    fig.add_hline(y=30, line=dict(color='red', dash='dash'), row=3, col=1)
    fig.add_hline(y=70, line=dict(color='red', dash='dash'), row=3, col=1)

    # RSI Al/Sat sinyalleri ekle
    for i in range(1, len(hist)):
        if hist['rsi_signal'].iloc[i] == 'Al' and hist['rsi_signal'].iloc[i-1] != 'Al':
            fig.add_annotation(
                x=hist.index[i],
                y=hist['rsi'].iloc[i],
                text='Al',
                showarrow=True,
                arrowhead=1,
                ax=0,
                ay=-30,
                font=dict(color='green'),
                row=3, col=1
            )
        elif hist['rsi_signal'].iloc[i] == 'Sat' and hist['rsi_signal'].iloc[i-1] != 'Sat':
            fig.add_annotation(
                x=hist.index[i],
                y=hist['rsi'].iloc[i],
                text='Sat',
                showarrow=True,
                arrowhead=1,
                ax=0,
                ay=30,
                font=dict(color='red'),
                row=3, col=1
            )

    # Bollinger Bands Al/Sat sinyalleri ekle
    for i in range(1, len(hist)):
        if hist['bb_signal'].iloc[i] == 'Al' and hist['bb_signal'].iloc[i-1] != 'Al':
            fig.add_annotation(
                x=hist.index[i],
                y=hist['lower_band'].iloc[i],
                text='Al',
                showarrow=True,
                arrowhead=1,
                ax=0,
                ay=-30,
                font=dict(color='green'),
                row=1, col=1
            )
        elif hist['bb_signal'].iloc[i] == 'Sat' and hist['bb_signal'].iloc[i-1] != 'Sat':
            fig.add_annotation(
                x=hist.index[i],
                y=hist['upper_band'].iloc[i],
                text='Sat',
                showarrow=True,
                arrowhead=1,
                ax=0,
                ay=30,
                font=dict(color='red'),
                row=1, col=1
            )

    # Add explanations as annotations
    fig.add_annotation(
        xref="paper", yref="paper",
        x=0.5, y=-0.25,
        showarrow=False,
        text=(
            "MACD: Hareketli ortalamalar arasındaki farkı ölçer. "
            "MACD sinyal çizgisini yukarı keserse 'Al', aşağı keserse 'Sat' sinyali verir.<br>"
            "RSI: Hissenin aşırı alım ya da aşırı satımda olup olmadığını gösterir. "
            "RSI 30'un altına düşerse 'Al', 70'in üstüne çıkarsa 'Sat' sinyali verir.<br>"
            "Bollinger Bantları: Fiyatın üst veya alt bantlara yaklaştığını gösterir. "
            "Fiyat alt bandın altına düşerse 'Al', üst bandın üstüne çıkarsa 'Sat' sinyali verir."
        ),
        font=dict(size=12)
    )

    fig.update_layout(title=f'Fiyat Değişim Grafiği - {stock_symbol}',
                      xaxis_title='Tarih',
                      yaxis_title='Fiyat',
                      xaxis_rangeslider_visible=False,
                      width=1400,
                      height=1000,
                      font=dict(
                          family="Arial, sans-serif",
                          size=14,
                          color="RebeccaPurple"
                      ),
                      title_font=dict(
                          size=24
                      ),
                      xaxis=dict(
                          title=dict(
                              font=dict(
                                  size=18
                              )
                          )
                      ),
                      yaxis=dict(
                          title=dict(
                              font=dict(
                                  size=18
                              )
                          )
                      ))

    # Son indikatör sinyallerini al
    last_macd_signal = hist['macd_signal'].iloc[-1]
    last_rsi_signal = hist['rsi_signal'].iloc[-1]
    last_bb_signal = hist['bb_signal'].iloc[-1]

    # Örnek veri listesi
    signals_summary = [
        f"MACD: {last_macd_signal}",
        f"RSI: {last_rsi_signal}",
        f"Bollinger Bands: {last_bb_signal}"
    ]


    buf = BytesIO()
    fig.write_image(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    return image_base64, signals_summary


