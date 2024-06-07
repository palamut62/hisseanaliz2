import os
from PIL import Image, ImageDraw, ImageFont
import random
import plotly.graph_objs as go
from datetime import datetime, timedelta
import io
import base64
import pandas as pd
import yfinance as yf
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands
from ta.trend import SMAIndicator
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import base64
from io import BytesIO


def initials_image(name):
    # Ad soyadı böl ve baş harfleri al
    name_split = name.split(' ')
    first_name = name_split[0]
    last_name = name_split[1]

    first_letter = first_name[0].upper()
    second_letter = last_name[0].upper()

    # Görsel boyutları
    img_width = 500
    img_height = 500

    # Arkaplan rengi
    r = random.randint(200, 255)
    g = random.randint(200, 255)
    b = random.randint(200, 255)
    bg_color = (r, g, b)

    # Yazı font boyutu
    font_size = img_width // 2

    # Yazıyı ortalamak için koordinatlar
    x = img_width // 2
    y = img_height // 2

    # Görsel oluştur
    img = Image.new('RGB', (img_width, img_height), color=bg_color)

    # Yazıyı ortaya yerleştir
    draw = ImageDraw.Draw(img)

    # Arkaplan rengi
    r, g, b = random.randint(200, 255), random.randint(200, 255), random.randint(200, 255)
    bg_color = (r, g, b)

    # Ortalama arkaplan rengini hesapla
    avg_bg = (r + g + b) // 3

    # Eğer açık renkse siyah, koyu renkse beyaz yazı rengi olarak belirle
    if avg_bg > 127:
        text_color = 'dimgray'
    else:
        text_color = 'white'

    # Yazı rengini belirlenen renkte çiz

    text = first_letter + second_letter
    draw.text((x, y), text, fill=text_color,
              font=ImageFont.truetype("arial.ttf", size=font_size),
              anchor="mm")

    # Görsel kaydet
    media_dir = os.path.join(os.getcwd(), 'media')
    image_path = os.path.join(media_dir, 'profil_picture.png')

    if not os.path.exists(media_dir):
        os.mkdir(media_dir)

    img.save(image_path)

    return image_path


import google.generativeai as genai

# Google Gemini API anahtarınızı burada yapılandırın
genai.configure(api_key="AIzaSyD8ac-8ReTvAYTJ-yYKgxaRGvgcUF3DNU4")
model = genai.GenerativeModel('gemini-1.5-flash-latest')


def hisse_bilgilerini_analiz_et(hisse_bilgisi):
    # Hisse bilgilerini düzenleyin ve analiz için uygun hale getirin



    prompt = (
            f"Aşağıdaki hisse bilgilerini analiz edin:\n\n"
            f"Sembol: {hisse_bilgisi.get('sembol')}\n"
            f"İsim: {hisse_bilgisi.get('isim')}\n"
            f"Sektör: {hisse_bilgisi.get('sektor')}\n"
            f"Fiyat: {hisse_bilgisi.get('fiyat')}\n"
            f"Piyasa Değeri: {hisse_bilgisi.get('piyasa_degeri')}\n"
            f"F/K Oranı: {hisse_bilgisi.get('fk_orani')}\n"
            f"EPS: {hisse_bilgisi.get('eps')}\n"
            f"Özsermaye Değeri: {hisse_bilgisi.get('ozsermaye')}\n"
            f"Net Gelir: {hisse_bilgisi.get('net_gelir')}\n"
            f"Toplam Varlıklar: {hisse_bilgisi.get('toplam_varliklar')}\n"
            f"Toplam Borçlar: {hisse_bilgisi.get('toplam_borclar')}\n"
            f"Gelir: {hisse_bilgisi.get('gelir')}\n"
            f"Adres: {hisse_bilgisi.get('address1')}, {hisse_bilgisi.get('address2')}, {hisse_bilgisi.get('city')}, {hisse_bilgisi.get('zip')}, {hisse_bilgisi.get('country')}\n"
            f"Telefon: {hisse_bilgisi.get('phone')}\n"
            f"Faks: {hisse_bilgisi.get('fax')}\n"
            f"Web Sitesi: {hisse_bilgisi.get('website')}\n"
            f"Endüstri: {hisse_bilgisi.get('industry')}\n"
            f"Çalışan Sayısı: {hisse_bilgisi.get('fullTimeEmployees')}\n"
            f"Mevcut Fiyat: {hisse_bilgisi.get('currentPrice')}\n"
            f"Yüksek Hedef Fiyat: {hisse_bilgisi.get('targetHighPrice')}\n"
            f"Düşük Hedef Fiyat: {hisse_bilgisi.get('targetLowPrice')}\n"
            f"Ortalama Hedef Fiyat: {hisse_bilgisi.get('targetMeanPrice')}\n"
            f"Medyan Hedef Fiyat: {hisse_bilgisi.get('targetMedianPrice')}\n"
            f"Öneri Ortalaması: {hisse_bilgisi.get('recommendationMean')}\n"
            f"Öneri Anahtarı: {hisse_bilgisi.get('recommendationKey')}\n"
            f"Analist Görüş Sayısı: {hisse_bilgisi.get('numberOfAnalystOpinions')}\n"
            f"Toplam Nakit: {hisse_bilgisi.get('totalCash')}\n"
            f"Hisse Başına Nakit: {hisse_bilgisi.get('totalCashPerShare')}\n"
            f"EBITDA: {hisse_bilgisi.get('ebitda')}\n"
            f"Hızlı Oran: {hisse_bilgisi.get('quickRatio')}\n"
            f"Mevcut Oran: {hisse_bilgisi.get('currentRatio')}\n"
            f"Toplam Gelir: {hisse_bilgisi.get('totalRevenue')}\n"
            f"Borç/Özsermaye Oranı: {hisse_bilgisi.get('debtToEquity')}\n"
            f"Hisse Başına Gelir: {hisse_bilgisi.get('revenuePerShare')}\n"
            f"Varlık Getirisi: {hisse_bilgisi.get('returnOnAssets')}\n"
            f"Özsermaye Getirisi: {hisse_bilgisi.get('returnOnEquity')}\n"
            f"Serbest Nakit Akışı: {hisse_bilgisi.get('freeCashflow')}\n"
            f"Faaliyet Nakit Akışı: {hisse_bilgisi.get('operatingCashflow')}\n"
            f"Kazanç Büyümesi: {hisse_bilgisi.get('earningsGrowth')}\n"
            f"Gelir Büyümesi: {hisse_bilgisi.get('revenueGrowth')}\n"
            f"Brüt Kar Marjı: {hisse_bilgisi.get('grossMargins')}\n"
            f"EBITDA Marjı: {hisse_bilgisi.get('ebitdaMargins')}\n"
            f"Faaliyet Kar Marjı: {hisse_bilgisi.get('operatingMargins')}\n\n"
            "Bu hisse senedinin güçlü ve zayıf yönlerini, yatırım potansiyelini içeren detaylı bir analiz ve değerlendirme yapın.Birde şu değerlendirmeyi yap sonuça göre Al,Tut,Sat şeklinde bir öneri ver.Ayrıca değerlendirmeyi kısa ve öz tut sadece en önemli kriterleri vurgula."
    )

    # Modelden içerik üretmesini isteyin
    response = model.generate_content(prompt)
    analiz = response.text

    # Metni HTML formatına dönüştür
    html_output = convert_to_html(analiz)

    return html_output




def convert_to_html(text):
    # Metni parçalara ayır
    lines = text.split('\n')
    html_lines = []

    for line in lines:
        line = line.strip()
        if line.startswith("**") and line.endswith("**:"):
            html_lines.append(f"<li><strong>{line.strip('**:')}</strong></li>")
        elif line.startswith("* **"):
            html_lines.append(f"<ul><li><strong>{line.strip('* **')}</strong></li></ul>")
        elif line.startswith("* "):
            html_lines.append(f"<li>{line.strip('* ')}</li>")
        else:
            html_lines.append(f"<li>{line}</li>")

    return "<ul>" + "\n".join(html_lines) + "</ul>"



pd.set_option('future.no_silent_downcasting', True)

def get_fd_favok_graph(stock_symbol):
    # Hisse kodunu belirtin
    ticker = stock_symbol

    # Hisse verisini çekin
    hisse = yf.Ticker(ticker)

    # Son 10 yıllık çeyrek dönem verilerini alın
    finansal_veri = hisse.quarterly_financials.T.iloc[:, :10]
    bilanco_veri = hisse.quarterly_balance_sheet.T.iloc[:, :10]

    # Gerekli sütunların mevcut olup olmadığını kontrol edin
    required_financial_columns = ["Net Income From Continuing Operation Net Minority Interest",
                                 "Reconciled Depreciation",
                                 "Amortization of Intangible Assets"]
    missing_financial_columns = [col for col in required_financial_columns if col not in finansal_veri.columns]

    # Eksik sütunlar için sıfır değerli sütunlar oluşturun
    for col in missing_financial_columns:
        finansal_veri[col] = pd.Series([0]*len(finansal_veri), index=finansal_veri.index)

    # Interest Expense sütunu opsiyonel olarak kontrol edilir
    if "Interest Expense" not in finansal_veri.columns:
        print("Opsiyonel sütun eksik: 'Interest Expense'")
        interest_expense = pd.Series([0]*len(finansal_veri), index=finansal_veri.index)
    else:
        interest_expense = finansal_veri["Interest Expense"]

    # EBITDA hesaplaması için gerekli verileri al
    net_income = finansal_veri["Net Income From Continuing Operation Net Minority Interest"].fillna(0).astype(float)
    depreciation = finansal_veri["Reconciled Depreciation"].fillna(0).astype(float)
    amortization = finansal_veri["Amortization of Intangible Assets"].fillna(0).astype(float)

    # EBITDA'yı hesapla
    ebitda = net_income + interest_expense + depreciation + amortization

    # Bilançodan Net Borç (Net Debt) verisini al
    if "Total Debt" not in bilanco_veri.columns:
        raise KeyError("Gerekli sütun eksik: 'Total Debt'")

    total_debt = bilanco_veri["Total Debt"].fillna(0).astype(float)

    # FD/FAVÖK oranını hesapla
    fd_favok_orani = total_debt / ebitda

    # Son 10 dönemin ortalamalarını hesapla
    fd_favok_orani_ortalama = fd_favok_orani.mean()

    # Grafik boyutlarını ayarlayın
    plt.figure(figsize=(10, 6))

    # Grafik başlığını belirleyin
    plt.title('FD/FAVÖK Grafiği')

    # Verileri çizin
    plt.plot(fd_favok_orani.index, fd_favok_orani.values, label='FD/FAVÖK Oranı', color='tab:red', marker='o')

    # Kesikli yatay çizgi oluşturma ve ortalama değeri gösterme
    plt.axhline(y=fd_favok_orani_ortalama, color='red', linestyle='--', label='FD/FAVÖK Oranı Ortalama:'+str(round(fd_favok_orani_ortalama,2)))
    plt.annotate(f'{fd_favok_orani_ortalama:.2f}',
                 xy=(fd_favok_orani.index[-1], fd_favok_orani_ortalama),
                 xytext=(10, 0), textcoords='offset points', ha='left', va='center',
                 fontsize=10, weight='bold', color='red')

    # Değerleri grafik üzerinde göster
    for i in range(len(fd_favok_orani)):
        plt.annotate(f'{fd_favok_orani.values[i]:.2f}', (fd_favok_orani.index[i], fd_favok_orani.values[i]),
                     textcoords="offset points", xytext=(0, 5), ha='center', fontsize=8)

    # Efsaneyi (legend) göster
    plt.xlabel('Dönem')
    plt.ylabel('FD/FAVÖK Oranı')
    plt.legend()
    plt.grid(True)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    plt.close()

    return image_base64







def get_price_change_graph(stock_symbol):
    stock = yf.Ticker(stock_symbol)
    hist = stock.history(period="1y")

    # Fiyat değişimlerini hesapla
    hist['PriceChange'] = hist['Close'].pct_change() * 100

    # %5'ten fazla değişim olan noktaları belirle
    breakpoints = hist[abs(hist['PriceChange']) > 5]

    fig = go.Figure(data=[go.Candlestick(x=hist.index,
                                         open=hist['Open'],
                                         high=hist['High'],
                                         low=hist['Low'],
                                         close=hist['Close'])])

    prev_bp = None
    # Yatay çizgiler ve etiketler ekle
    for index, row in breakpoints.iterrows():
        fig.add_shape(
            type="line",
            x0=hist.index[0],
            y0=row['Close'],
            x1=hist.index[-1],
            y1=row['Close'],
            line=dict(
                color="rgba(255, 0, 0, 0.5)",  # Red rengini %50 opaklık ile ayarlayın
                width=1,
                dash="dashdot"

            )
        )
        fig.add_annotation(
            x=index,
            y=row['Close'],
            text=f'{row["Close"]:.2f}',
            showarrow=True,
            arrowhead=1,
            ax=0,
            ay=-30,
            bgcolor="rgba(255, 255, 255, 0.7)"
        )

        if prev_bp is not None:
            change_percentage = ((row['Close'] - prev_bp['Close']) / prev_bp['Close']) * 100
            color = "green" if change_percentage > 0 else "red"
            fig.add_annotation(
                x=index,
                y=(row['Close'] + prev_bp['Close']) / 2,
                text=f'{change_percentage:.2f}%',
                showarrow=False,
                font=dict(color=color),
                bgcolor="rgba(255, 255, 255, 0.7)"
            )

        prev_bp = row

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

    buf = BytesIO()
    fig.write_image(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    return image_base64


def get_monthly_performance(stock_symbol):
    stock = yf.Ticker(stock_symbol)
    hist = stock.history(period="1mo")

    # Performansı hesapla
    start_price = hist['Close'].iloc[0]
    end_price = hist['Close'].iloc[-1]
    performance = ((end_price - start_price) / start_price) * 100

    performance_evaluation = "Artış" if performance > 0 else "Azalış" if performance < 0 else "Değişim Yok"

    return {
        'start_price': start_price,
        'end_price': end_price,
        'performance': performance,
        'performance_evaluation': performance_evaluation
    }





def get_recently_listed_stocks():
    # Örnek semboller (Bu listeyi güncelleyerek daha fazla sembol ekleyebilirsiniz)
    tickers_list = ['ABNB', 'PLTR', 'SNOW', 'AI', 'UBER']  # Örnek semboller
    tickers = yf.Tickers(tickers_list)

    # Tüm hisse senedi verilerini çek
    data = {ticker: tickers.tickers[ticker].info for ticker in tickers_list}
    all_stocks = pd.DataFrame.from_dict(data, orient='index')

    # Halka arz tarihi olanları filtrele
    if 'ipoDate' not in all_stocks.columns:
        raise KeyError("'ipoDate' sütunu veri setinde bulunamadı.")

    # Halka arz tarihi olanları filtrele
    all_stocks['ipoDate'] = pd.to_datetime(all_stocks['ipoDate'], errors='coerce')
    ipo_date_threshold = datetime.now() - timedelta(days=60)
    recently_listed = all_stocks[all_stocks['ipoDate'] > ipo_date_threshold]

    if recently_listed.empty:
        return pd.DataFrame()  # Boş bir DataFrame döndür

    # Gerekli bilgileri döndür
    return recently_listed[['symbol', 'ipoDate', 'shortName', 'sector']]


def fetch_and_predict_stock_data(symbol, start_date, end_date):
    # Yfinance ile veri çekme
    data = yf.download(symbol, start=start_date, end=end_date)

    # İlgili sütunları seçme ve indikatör hesaplama
    data['RSI'] = RSIIndicator(close=data['Close'], window=14).rsi()
    data['SMA'] = SMAIndicator(close=data['Close'], window=20).sma_indicator()
    bb = BollingerBands(close=data['Close'], window=20, window_dev=2)
    data['BB_High'] = bb.bollinger_hband()
    data['BB_Low'] = bb.bollinger_lband()

    # Temel analiz verileri
    stock_info = yf.Ticker(symbol).info
    data['P/E'] = stock_info.get('trailingPE', None)
    data['Market_Cap'] = stock_info.get('marketCap', None)
    data['EPS'] = stock_info.get('trailingEps', None)

    # NaN değerleri çıkarma
    data = data.dropna()

    # Özellikleri ve hedefi belirleme
    X = data[['Close', 'Volume', 'RSI', 'SMA', 'BB_High', 'BB_Low', 'P/E', 'Market_Cap', 'EPS']]
    y = data['Close']

    # Veri setini eğitim ve test olarak bölme
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model eğitimi
    model = DecisionTreeRegressor()
    model.fit(X_train, y_train)

    # Tahmin
    y_pred = model.predict(X_test)

    # Modelin performansını kontrol etme
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error: {mse:.2f}")

    # Grafik çizme ve kaydetme (Gerçek ve Tahmin Edilen Değerler)
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(data.index, data['Close'], label='Gerçek Fiyatlar')
    ax.plot(X_test.index, y_pred, label='Tahmin Edilen Fiyatlar', color='orange')
    ax.set_xlabel('Tarih')
    ax.set_ylabel('Fiyat')
    ax.set_title(f'{symbol} Fiyat Tahminleri')
    ax.legend()

    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    price_change_grafic = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close(fig)

    # Bir haftalık ileri tarih fiyat tahmini
    future_dates = pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=7)
    future_data = pd.DataFrame(index=future_dates, columns=X.columns)

    # Gelecek verilerde, son gözlemlenen verileri kullanarak tahmin yapıyoruz
    last_observation = X.iloc[-1]
    for column in future_data.columns:
        future_data[column] = last_observation[column]

    future_prices = model.predict(future_data)

    # Gelecek fiyatların grafiğini çizme ve kaydetme
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(data.index, data['Close'], label='Gerçek Fiyatlar')
    ax.plot(future_dates, future_prices, label='Gelecek Tahmin Edilen Fiyatlar', color='red')
    ax.set_xlabel('Tarih')
    ax.set_ylabel('Fiyat')
    ax.set_title(f'{symbol} Gelecek Fiyat Tahminleri')
    ax.legend()

    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    future_stock_prediction = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close(fig)

    return mse, price_change_grafic, future_stock_prediction











