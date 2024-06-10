import yfinance as yf
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


def get_stock_details(ticker):
    """
    Hisse senedine ait tüm bilgileri toplar.

    Args:
        ticker: Hisse senedi sembolü (örneğin, "AAPL")

    Returns:
        Hisse senedinin özellikleri içeren bir sözlük.
    """

    stock = yf.Ticker(ticker)
    info = stock.info
    historical_data = stock.actions  # Temettü, hisse bölünmesi gibi eylemleri al
    # Temel Bilgiler
    basic_info = {
        "Hisse Senedi Adı": info["longName"],
        "Sembol": info["symbol"],
        "Sektör": info["sector"],
        "Alt Sektör": info["industry"],
        "Borsa": info["exchange"],
        "Para Birimi": info["currency"],
        "Web Sitesi": info["website"],
        "Son Kapanış": info["currentPrice"],
        "Günlük Değişim (%)": f"({info['regularMarketDayLow']} - {info['regularMarketDayHigh']})",
        "52 Hafta Yüksek": info["fiftyTwoWeekHigh"],
        "52 Hafta Düşük": info["fiftyTwoWeekLow"],
        "Piyasa Değeri": info["marketCap"],
        # "Temettü Verimi": info["dividendYield"],
        # "Son Temettü": info["trailingAnnualDividendRate"],
        # "Temettü Ödeme Tarihi": historical_data[historical_data['Dividends'] != 0].index,
        # "Temettü Ex-Date": info["exDividendDate"],
        "Çalışan Sayısı": info["fullTimeEmployees"],
        "Yönetim Kurulu": get_board_members(ticker),
    }

    # Finansal Bilgiler
    financial_data = {
        "Gelir (Son Çeyrek)": info["totalRevenue"],
        "Kar (Son Çeyrek)": info["netIncomeToCommon"],
        "Kâr Marjı": info["profitMargins"],
        "Gelir Büyümesi (Yıllık)": info["revenueGrowth"],
        "Kar Büyümesi (Yıllık)": info["earningsGrowth"],
        "Öz Sermaye Getirisi": info["returnOnEquity"],
        "Borç/Öz Sermaye Oranı": info["debtToEquity"],
        "Cari Oran": info["currentRatio"],
        "Hızlı Oran": info["quickRatio"],
        "Nakit Akışı (İşletmeden)": stock.cashflow.iloc[-1].get("Cash Flow from Operating Activities", "Veri mevcut değil"),
        "Nakit Akışı (Yatırımdan)": stock.cashflow.iloc[-1].get("Total Cash From Investing Activities", "Veri mevcut değil"),
        "Nakit Akışı (Finansmandan)": stock.cashflow.iloc[-1].get("Total Cash From Financing Activities", "Veri mevcut değil")


    }

    # Fiyat Geçmişi
    historical_data = stock.history(period="max")
    price_history = {
        "Açılış": historical_data["Open"].iloc[-1],
        "Kapanış": historical_data["Close"].iloc[-1],
        "Yüksek": historical_data["High"].iloc[-1],
        "Düşük": historical_data["Low"].iloc[-1],
        "İşlem Hacmi": historical_data["Volume"].iloc[-1],
        "50 Gün Hareketli Ortalama": historical_data["Close"].rolling(window=50).mean().iloc[-1],
        "200 Gün Hareketli Ortalama": historical_data["Close"].rolling(window=200).mean().iloc[-1],
    }

    # Teknik Göstergeler
    technical_indicators = {
        "RSI (14 Gün)": calculate_rsi(historical_data["Close"], period=14),
        "MACD (12-26-9)": calculate_macd(historical_data["Close"], fastperiod=12, slowperiod=26, signalperiod=9),
        "Stokastik Osilatör (%K)":
            calculate_stochastic_oscillator(historical_data["Close"], historical_data["High"], historical_data["Low"],
                                            period=14)[0],
        "Stokastik Osilatör (%D)":
            calculate_stochastic_oscillator(historical_data["Close"], historical_data["High"], historical_data["Low"],
                                            period=14)[1],
        "Bollinger Bantları Üst": calculate_bollinger_bands(historical_data["Close"], period=20)[0],
        "Bollinger Bantları Orta": calculate_bollinger_bands(historical_data["Close"], period=20)[1],
        "Bollinger Bantları Alt": calculate_bollinger_bands(historical_data["Close"], period=20)[2],
        "ADX (14 Gün)": calculate_adx(historical_data["High"], historical_data["Low"], historical_data["Close"],
                                      period=14),
        "CCI (20 Gün)": calculate_cci(historical_data["High"], historical_data["Low"], historical_data["Close"],
                                      period=20),
        "Aroon Üst": calculate_aroon(historical_data["High"], period=25)[0],
        "Aroon Alt": calculate_aroon(historical_data["High"], period=25)[1],
    }

    # Haberler
    news_url = f"https://finance.yahoo.com/quote/{ticker}/news"
    response = requests.get(news_url)
    soup = BeautifulSoup(response.content, "html.parser")
    news_items = soup.find_all("a", class_="Fw(b) Fz(18px) Lh(1.3)")
    news_data = []
    for item in news_items:
        news_data.append({
            "Başlık": item.text,
            "Bağlantı": item["href"],
        })

    # Analist Tahminleri
    analyst_url = f"https://finance.yahoo.com/quote/{ticker}/analysis"
    response = requests.get(analyst_url)
    soup = BeautifulSoup(response.content, "html.parser")
    analyst_data = {}
    try:
        # Analist hedef fiyat bilgisi
        target_price = soup.find("td", class_="Ta(end) Fw(b) Fz(16px) Lh(1.4)").text
        analyst_data["Hedef Fiyat"] = target_price
        # Analist görüşleri (Al, Tut, Sat)
        analyst_ratings = soup.find_all("td", class_="Va(m) Ta(end) Fw(b) Fz(16px) Lh(1.4)")
        for rating in analyst_ratings:
            try:
                rating_type = rating.find_previous("span", class_="C($tertiaryColor)").text.strip()
                rating_value = rating.text.strip()
                analyst_data[rating_type] = rating_value
            except:
                pass
    except:
        pass

    # Ek Bilgiler
    additional_info = {
        "Şirket Açıklaması": get_company_description(ticker),
        "Kilit Çalışanlar": get_key_employees(ticker),
        "Finansal Raporlar": get_financial_reports(ticker),
        # Daha fazla özel bilgi eklenebilir
    }

    all_details = {
        **basic_info,
        **financial_data,
        **price_history,
        "Teknik Göstergeler": technical_indicators,  # Bu satırı ekleyin
        "Haberler": news_data,
        "Analist Tahminleri": analyst_data,
        **additional_info,
        "stock": stock
    }
    return all_details


def calculate_rsi(prices, period=14):
    """
    RSI (Göreli Güç Endeksi) hesaplar.

    Args:
        prices: Fiyat serisi (pandas.Series).
        period: RSI dönemi.

    Returns:
        RSI değeri.
    """
    delta = prices.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    avg_gain = up.rolling(window=period).mean()
    avg_loss = down.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]


def calculate_macd(prices, fastperiod=12, slowperiod=26, signalperiod=9):
    """
    MACD (Hareketli Ortalamalar Yakınsama Uzaklaşma) hesaplar.

    Args:
        prices: Fiyat serisi (pandas.Series).
        fastperiod: Hızlı hareketli ortalama için dönem.
        slowperiod: Yavaş hareketli ortalama için dönem.
        signalperiod: Sinyal çizgisi için dönem.

    Returns:
        MACD değeri.
    """
    macd_line = prices.ewm(span=fastperiod, adjust=False).mean() - prices.ewm(span=slowperiod, adjust=False).mean()
    signal_line = macd_line.ewm(span=signalperiod, adjust=False).mean()
    macd = macd_line - signal_line
    return macd.iloc[-1]


def calculate_stochastic_oscillator(close, high, low, period=14):
    """
    Stokastik Osilatör hesaplar.

    Args:
        close: Kapanış fiyatları (pandas.Series).
        high: Yüksek fiyatlar (pandas.Series).
        low: Düşük fiyatlar (pandas.Series).
        period: Stokastik osilatör dönemi.

    Returns:
        Stokastik osilatör %K ve %D değerleri.
    """
    lowest_low = low.rolling(window=period).min()
    highest_high = high.rolling(window=period).max()
    k = (close - lowest_low) / (highest_high - lowest_low) * 100
    d = k.rolling(window=3).mean()
    return k.iloc[-1], d.iloc[-1]


def calculate_bollinger_bands(prices, period=20):
    """
    Bollinger Bantları hesaplar.

    Args:
        prices: Fiyat serisi (pandas.Series).
        period: Bollinger bantları dönemi.

    Returns:
        Bollinger bantlarının üst, orta ve alt sınırları.
    """
    sma = prices.rolling(window=period).mean()
    std = prices.rolling(window=period).std()
    upper_band = sma + 2 * std
    middle_band = sma
    lower_band = sma - 2 * std
    return upper_band.iloc[-1], middle_band.iloc[-1], lower_band.iloc[-1]


def calculate_adx(high, low, close, period=14):
    """
    ADX (Ortalama Yönlü Hareket Endeksi) hesaplar.

    Args:
        high: Yüksek fiyatlar (pandas.Series).
        low: Düşük fiyatlar (pandas.Series).
        close: Kapanış fiyatları (pandas.Series).
        period: ADX dönemi.

    Returns:
        ADX değeri.
    """
    # True Range hesapla
    tr = pd.DataFrame({
        "tr1": abs(high - low),
        "tr2": abs(high - close.shift()),
        "tr3": abs(low - close.shift()),
    }).max(axis=1)

    # +DM ve -DM hesapla
    plus_dm = (high - high.shift()).clip(lower=0)
    minus_dm = (low.shift() - low).clip(lower=0)

    # DM'lerin en büyük değerini al
    plus_dm_max = plus_dm.where(plus_dm > minus_dm, 0)
    minus_dm_max = minus_dm.where(minus_dm > plus_dm, 0)

    # DM'lerin hareketli ortalamaları
    tr_avg = tr.rolling(window=period).mean()
    plus_dm_avg = plus_dm_max.rolling(window=period).mean()
    minus_dm_avg = minus_dm_max.rolling(window=period).mean()

    # +DI ve -DI hesapla
    plus_di = 100 * (plus_dm_avg / tr_avg)
    minus_di = 100 * (minus_dm_avg / tr_avg)

    # DX hesapla
    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)

    # ADX hesapla
    adx = dx.rolling(window=period).mean()
    return adx.iloc[-1]


def calculate_cci(high, low, close, period=20):
    """
    CCI (Malzeme Geliştirme Endeksi) hesaplar.

    Args:
        high: Yüksek fiyatlar (pandas.Series).
        low: Düşük fiyatlar (pandas.Series).
        close: Kapanış fiyatları (pandas.Series).
        period: CCI dönemi.

    Returns:
        CCI değeri.
    """
    tp = (high + low + close) / 3
    sma = tp.rolling(window=period).mean()
    md = abs(tp - sma).rolling(window=period).mean() * 0.015
    cci = (tp - sma) / md
    return cci.iloc[-1]


def calculate_aroon(high, period=25):
    """
    Aroon Üst ve Alt hesaplar.

    Args:
        high: Yüksek fiyatlar (pandas.Series).
        period: Aroon dönemi.

    Returns:
        Aroon Üst ve Alt değerleri.
    """
    highest_high = high.rolling(window=period).apply(lambda x: x.argmax())
    lowest_low = high.rolling(window=period).apply(lambda x: x.argmin())
    aroon_up = 100 * (period - highest_high) / period
    aroon_down = 100 * (period - lowest_low) / period
    return aroon_up.iloc[-1], aroon_down.iloc[-1]


def get_board_members(ticker):
    """
    Şirketin yönetim kurulu üyelerini toplar.

    Args:
        ticker: Hisse senedi sembolü.

    Returns:
        Yönetim kurulu üyelerinin isimlerini içeren bir liste.
    """
    board_members = []
    # Şirketin web sitesinden yönetim kurulu üyeleri hakkında bilgi çekmek için kod eklenebilir.
    return board_members


import requests
from bs4 import BeautifulSoup

def get_company_description(ticker):
    """
    Şirketin açıklamasını çeker.

    Args:
        ticker: Hisse senedi sembolü.

    Returns:
        Şirket açıklaması.
    """
    url = f"https://finance.yahoo.com/quote/{ticker}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    try:
        # Alternatif seçici kullanarak
        description = soup.find("p", class_="Mt(15px) Mb(10px)").text
        # veya
        # description = soup.find("p", class_="D(ib) Mend(20px)").text # Farklı bir class dene
    except AttributeError:
        description = "Şirket açıklaması bulunamadı."

    return description


def get_key_employees(ticker):
    """
    Şirketin kilit çalışanlarını çeker.

    Args:
        ticker: Hisse senedi sembolü.

    Returns:
        Kilit çalışanların isimlerini içeren bir liste.
    """
    key_employees = []
    # Şirketin web sitesinden kilit çalışanlar hakkında bilgi çekmek için kod eklenebilir.
    return key_employees


def get_financial_reports(ticker):
    """
    Şirketin finansal raporlarını çeker.

    Args:
        ticker: Hisse senedi sembolü.

    Returns:
        Finansal raporların bağlantılarını içeren bir liste.
    """
    financial_reports = []
    # Şirketin web sitesinden finansal raporlar hakkında bilgi çekmek için kod eklenebilir.
    return financial_reports


def plot_price_and_indicators(historical_data, ticker):
    """
    Hisse senedi fiyatı ve teknik göstergeleri çizerek görselleştirir.

    Args:
        historical_data: Yfinance'dan alınan tarihsel fiyat verileri.
        ticker: Hisse senedi sembolü.
    """
    plt.figure(figsize=(12, 8))

    # Fiyat grafiğini çiz
    plt.subplot(3, 1, 1)
    plt.plot(historical_data["Close"], label="Kapanış Fiyatı")
    plt.title(f"{ticker} Hisse Senedi Fiyatı")
    plt.xlabel("Tarih")
    plt.ylabel("Fiyat")

    # 50 gün ve 200 gün hareketli ortalamaları ekle
    plt.plot(historical_data["Close"].rolling(window=50).mean(), label="50 Gün MA")
    plt.plot(historical_data["Close"].rolling(window=200).mean(), label="200 Gün MA")

    # Bollinger Bantları ekle
    upper_band, middle_band, lower_band = calculate_bollinger_bands(historical_data["Close"], period=20)
    plt.plot(upper_band, label="Üst Bollinger Bandı", linestyle="--")
    plt.plot(middle_band, label="Orta Bollinger Bandı", linestyle="--")
    plt.plot(lower_band, label="Alt Bollinger Bandı", linestyle="--")

    # MACD grafiğini alt kısma ekle
    macd = calculate_macd(historical_data["Close"], fastperiod=12, slowperiod=26, signalperiod=9)
    plt.subplot(3, 1, 2)
    plt.plot(macd, label="MACD")
    plt.title("MACD")
    plt.ylabel("MACD Değeri")

    # RSI grafiğini alt kısma ekle
    rsi = calculate_rsi(historical_data["Close"], period=14)
    plt.subplot(3, 1, 3)
    plt.plot(rsi, label="RSI")
    plt.title("Göreli Güç Endeksi (RSI)")
    plt.ylabel("RSI Değeri")
    plt.ylim(0, 100)

    # Efsaneyi göster
    plt.legend()
    plt.show()


if __name__ == "__main__":
    ticker = "THYAO.IS"  # Hisse senedi sembolünü buraya girin
    stock_details = get_stock_details(ticker)
    stock = stock_details["stock"]  # stock_details sözlüğünden stock'u alın    stock_details = get_stock_details(ticker)

    # Bilgileri yazdır
    print("Temel Bilgiler:")
    for key, value in stock_details.items():
        if isinstance(value, list):
            print(f"  {key}:")
            for item in value:
                print(f"    {item}")
        elif isinstance(value, dict):
            print(f"  {key}:")
            for k, v in value.items():
                print(f"    {k}: {v}")
        else:
            print(f"  {key}: {value}")

    # Teknik Gösterge Tablosunu Oluştur
    print("\nTeknik Göstergeler:")
    technical_indicators_df = pd.DataFrame.from_dict(stock_details["Teknik Göstergeler"], orient="index",
                                                     columns=["Değer"])
    print(technical_indicators_df)

    # Fiyat ve göstergeleri çiz
    plot_price_and_indicators(stock.history(period="max"), ticker)