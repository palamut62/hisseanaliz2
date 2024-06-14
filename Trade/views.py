import os
from types import SimpleNamespace
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from Trade.forms import StockForm, AddStockForm, SettingsForm
from Trade.models import Hisse, Settings
import yfinance as yf
from Trade.utils import hisse_bilgilerini_analiz_et
from bilanco import hisse_cek


def index(request):
    stocks = Hisse.objects.all()
    summary_data = None
    hisse_bilgisi = None
    selected_stock = None
    form = StockForm(request.POST or None)
    add_stock_form = AddStockForm(request.POST or None)

    if request.method == 'POST':
        if 'symbol' in request.POST:
            if form.is_valid():
                selected_stock = form.cleaned_data['symbol']
        else:
            if add_stock_form.is_valid():
                add_stock_form.save()
                return redirect('index')  # Form başarıyla gönderildikten sonra sayfayı yeniler
    else:
        if stocks:
            selected_stock = stocks.first().sembol

    selected_stock_file = None

    if selected_stock:
        ticker = yf.Ticker(selected_stock+ '.IS')
        info = ticker.info

        # Hisse bilgisi
        hisse_bilgisi_dict = {
            'sembol': selected_stock,
            'isim': info.get('longName', 'N/A'),
            'sektor': info.get('sector', 'N/A'),
            'fiyat': info.get('currentPrice', 'N/A'),
            'piyasa_degeri': info.get('marketCap', 'N/A'),
            'fk_orani': info.get('forwardPE', 'N/A'),
            'eps': info.get('trailingEps', 'N/A'),
            'ozsermaye': info.get('bookValue', 'N/A'),
            'net_gelir': info.get('netIncomeToCommon', 'N/A'),
            'toplam_varliklar': info.get('totalAssets', 'N/A'),
            'toplam_borclar': info.get('totalDebt', 'N/A'),
            'adres1': info.get('address1', 'N/A'),
            'adres2': info.get('address2', 'N/A'),
            'sehir': info.get('city', 'N/A'),
            'posta_kodu': info.get('zip', 'N/A'),
            'ulke': info.get('country', 'N/A'),
            'telefon': info.get('phone', 'N/A'),
            'faks': info.get('fax', 'N/A'),
            'web_sitesi': info.get('website', 'N/A'),
            'endustri': info.get('industry', 'N/A'),
            'fullTimeEmployees': info.get('fullTimeEmployees', 'N/A'),
            'is_ozeti': info.get('longBusinessSummary', 'N/A'),
        }

        hisse_bilgisi = SimpleNamespace(**hisse_bilgisi_dict)

        # Summary verileri
        summary_data = {
            'name': info.get('longName', 'N/A'),
            'currentPrice': info.get('currentPrice', 'N/A'),
            'targetHighPrice': info.get('targetHighPrice', 'N/A'),
            'targetLowPrice': info.get('targetLowPrice', 'N/A'),
            'targetMeanPrice': info.get('targetMeanPrice', 'N/A'),
            'targetMedianPrice': info.get('targetMedianPrice', 'N/A'),
            'recommendationMean': info.get('recommendationMean', 'N/A'),
            'recommendationKey': info.get('recommendationKey', 'N/A'),
            'numberOfAnalystOpinions': info.get('numberOfAnalystOpinions', 'N/A'),
            'totalCash': info.get('totalCash', 'N/A'),
            'totalCashPerShare': info.get('totalCashPerShare', 'N/A'),
            'ebitda': info.get('ebitda', 'N/A'),
            'totalDebt': info.get('totalDebt', 'N/A'),
            'quickRatio': info.get('quickRatio', 'N/A'),
            'currentRatio': info.get('currentRatio', 'N/A'),
            'totalRevenue': info.get('totalRevenue', 'N/A'),
            'debtToEquity': info.get('debtToEquity', 'N/A'),
            'revenuePerShare': info.get('revenuePerShare', 'N/A'),
            'returnOnAssets': info.get('returnOnAssets', 'N/A'),
            'returnOnEquity': info.get('returnOnEquity', 'N/A'),
            'freeCashflow': info.get('freeCashflow', 'N/A'),
            'operatingCashflow': info.get('operatingCashflow', 'N/A'),
            'earningsGrowth': info.get('earningsGrowth', 'N/A'),
            'revenueGrowth': info.get('revenueGrowth', 'N/A'),
            'grossMargins': info.get('grossMargins', 'N/A'),
            'ebitdaMargins': info.get('ebitdaMargins', 'N/A'),
            'operatingMargins': info.get('operatingMargins', 'N/A'),
        }
        semboller=[]
        for sembol in stocks:
            semboller.append(sembol.sembol)


        hisse_cek(semboller)

        selected_stock_file = selected_stock + '.xlsx'





    return render(request, 'index.html', {
        'form': form,
        'add_stock_form': add_stock_form,
        'stocks': stocks,
        'summary_data': summary_data,
        'hisse_bilgisi': hisse_bilgisi,
        'selected_stock': selected_stock,
        'selected_stock_file': selected_stock_file

    })



from django.http import JsonResponse, HttpResponse, Http404


def fetch_analysis(request):
    selected_stock = None
    stocks = Hisse.objects.all()

    if stocks:
        selected_stock = stocks.first().sembol

    if selected_stock:
        ticker = yf.Ticker(selected_stock)
        info = ticker.info
        summary_data = {
            'name': info.get('longName', 'N/A'),
            'currentPrice': info.get('currentPrice', 'N/A'),
            'targetHighPrice': info.get('targetHighPrice', 'N/A'),
            'targetLowPrice': info.get('targetLowPrice', 'N/A'),
            'targetMeanPrice': info.get('targetMeanPrice', 'N/A'),
            'targetMedianPrice': info.get('targetMedianPrice', 'N/A'),
            'recommendationMean': info.get('recommendationMean', 'N/A'),
            'recommendationKey': info.get('recommendationKey', 'N/A'),
            'numberOfAnalystOpinions': info.get('numberOfAnalystOpinions', 'N/A'),
            'totalCash': info.get('totalCash', 'N/A'),
            'totalCashPerShare': info.get('totalCashPerShare', 'N/A'),
            'ebitda': info.get('ebitda', 'N/A'),
            'totalDebt': info.get('totalDebt', 'N/A'),
            'quickRatio': info.get('quickRatio', 'N/A'),
            'currentRatio': info.get('currentRatio', 'N/A'),
            'totalRevenue': info.get('totalRevenue', 'N/A'),
            'debtToEquity': info.get('debtToEquity', 'N/A'),
            'revenuePerShare': info.get('revenuePerShare', 'N/A'),
            'returnOnAssets': info.get('returnOnAssets', 'N/A'),
            'returnOnEquity': info.get('returnOnEquity', 'N/A'),
            'freeCashflow': info.get('freeCashflow', 'N/A'),
            'operatingCashflow': info.get('operatingCashflow', 'N/A'),
            'earningsGrowth': info.get('earningsGrowth', 'N/A'),
            'revenueGrowth': info.get('revenueGrowth', 'N/A'),
            'grossMargins': info.get('grossMargins', 'N/A'),
            'ebitdaMargins': info.get('ebitdaMargins', 'N/A'),
            'operatingMargins': info.get('operatingMargins', 'N/A'),
        }
        google_gemini_degerlendirme = hisse_bilgilerini_analiz_et(summary_data)
        return JsonResponse({'analysis': google_gemini_degerlendirme, 'stock_name': summary_data['name']})

    return JsonResponse({'analysis': 'No stock selected', 'stock_name': 'N/A'})


def stock_table(request):
    stocks = Hisse.objects.all()
    stock_data = []

    for stock in stocks:
        ticker = yf.Ticker(stock.sembol)
        info = ticker.info

        # Temel analiz bilgilerini hesapla ve ekle
        try:
            current_ratio = info.get('currentAssets', 0) / info.get('currentLiabilities', 1)
            quick_ratio = (info.get('currentAssets', 0) - info.get('inventory', 0)) / info.get('currentLiabilities', 1)
            receivables_turnover = info.get('totalRevenue', 0) / info.get('receivables', 1)
            inventory_turnover = info.get('costOfRevenue', 0) / info.get('inventory', 1)
            asset_turnover = info.get('totalRevenue', 0) / info.get('totalAssets', 1)
            debt_to_equity = info.get('totalDebt', 0) / info.get('totalEquity', 1)
            interest_coverage = info.get('ebit', 0) / info.get('interestExpense', 1)
            pe_ratio = info.get('currentPrice', 0) / info.get('trailingEps', 1)
            pb_ratio = info.get('marketCap', 0) / info.get('bookValue', 1)
            ev_ebitda = info.get('enterpriseValue', 0) / info.get('ebitda', 1)
        except (ZeroDivisionError, TypeError):
            current_ratio = quick_ratio = receivables_turnover = inventory_turnover = asset_turnover = debt_to_equity = interest_coverage = pe_ratio = pb_ratio = ev_ebitda = 0

        recommendation_mean = info.get('recommendationMean', 3)
        if recommendation_mean <= 2.0:
            recommendation = 'Al'
        elif recommendation_mean >= 3.0:
            recommendation = 'Sat'
        else:
            recommendation = 'Tut'

        stock_data.append({
            'sembol': stock.sembol,
            'isim': info.get('longName', 'N/A'),
            'current_ratio': current_ratio,
            'quick_ratio': quick_ratio,
            'receivables_turnover': receivables_turnover,
            'inventory_turnover': inventory_turnover,
            'asset_turnover': asset_turnover,
            'debt_to_equity': debt_to_equity,
            'interest_coverage': interest_coverage,
            'pe_ratio': pe_ratio,
            'pb_ratio': pb_ratio,
            'ev_ebitda': ev_ebitda,
            'recommendation': recommendation
        })

    add_stock_form = AddStockForm()

    return render(request, 'stock_table.html', {
        'stock_data': stock_data,
        'add_stock_form': add_stock_form
    })


def temettu_tablosu(request):
    hisseler = Hisse.objects.all()
    temettu_verileri = []

    toplam_temettu = 0

    for hisse in hisseler:
        ticker = yf.Ticker(hisse.sembol)
        dividends = ticker.dividends

        if not dividends.empty:
            latest_dividend = dividends[-1]
        else:
            latest_dividend = 0

        lot_sayisi = hisse.lot_adedi
        temettu_miktari = latest_dividend * lot_sayisi  # Kullanıcı tarafından girilen lot sayısı ile hesapla
        toplam_temettu += temettu_miktari

        temettu_verileri.append({
            'isim': hisse.isim,
            'temettu_degeri': latest_dividend,
            'lot_sayisi': lot_sayisi,
            'temettu_miktari': temettu_miktari
        })

    context = {
        'temettu_verileri': temettu_verileri,
        'toplam_temettu': toplam_temettu,
    }

    return render(request, 'temettu_tablosu.html', context)


@csrf_exempt
def update_lot_adedi(request):
    if request.method == 'POST':
        hisse_adi = request.POST.get('hisse_adi')
        lot_adedi = request.POST.get('lot_adedi')
        try:
            hisse = Hisse.objects.get(isim=hisse_adi)
            hisse.lot_adedi = int(lot_adedi)
            hisse.save()
            return JsonResponse({'status': 'success'})
        except Hisse.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'Hisse bulunamadı'})
    return JsonResponse({'status': 'fail', 'message': 'Geçersiz istek'})


def calculate_bollinger_bands(data, window, std_dev):
    rolling_mean = data['Close'].rolling(window).mean()
    rolling_std = data['Close'].rolling(window).std()
    data['Bollinger Middle'] = rolling_mean
    data['Bollinger High'] = rolling_mean + (rolling_std * std_dev)
    data['Bollinger Low'] = rolling_mean - (rolling_std * std_dev)
    return data


def calculate_rsi(data, window):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    data['RSI'] = rsi
    return data


def calculate_macd(data, short_window, long_window, signal_window):
    data['EMA12'] = data['Close'].ewm(span=short_window, adjust=False).mean()
    data['EMA26'] = data['Close'].ewm(span=long_window, adjust=False).mean()
    data['MACD'] = data['EMA12'] - data['EMA26']
    data['Signal Line'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()
    return data


def mum_grafik(request):
    sembol = request.GET.get('sembol', None)
    period = request.GET.get('period', '1y')  # Varsayılan 1 yıl
    interval = '1d'  # Varsayılan günlük
    window = int(request.GET.get('window', 20))
    std_dev = int(request.GET.get('std_dev', 2))
    rsi_window = int(request.GET.get('rsi_window', 14))
    short_window = int(request.GET.get('short_window', 12))
    long_window = int(request.GET.get('long_window', 26))
    signal_window = int(request.GET.get('signal_window', 9))

    if period in ['1d', '5d']:
        interval = '1h'  # 1 günlük veya 5 günlük seçildiğinde saatlik
    elif period in ['1h', '4h', '8h']:
        interval = period  # 1 saat, 4 saat, 8 saat

    data = None

    if sembol:
        ticker = yf.Ticker(sembol)
        hist = ticker.history(period=period, interval=interval)  # Seçilen zaman periyoduna ve intervale göre veriyi çek
        hist = calculate_bollinger_bands(hist, window, std_dev)
        hist = calculate_rsi(hist, rsi_window)
        hist = calculate_macd(hist, short_window, long_window, signal_window)

        # NaN değerleri kaldırın
        hist = hist.dropna()

        data = {
            'dates': hist.index.strftime('%Y-%m-%d %H:%M:%S').tolist(),
            'open': hist['Open'].tolist(),
            'high': hist['High'].tolist(),
            'low': hist['Low'].tolist(),
            'close': hist['Close'].tolist(),
            'volume': hist['Volume'].tolist(),
            'bollinger_middle': hist['Bollinger Middle'].tolist(),
            'bollinger_high': hist['Bollinger High'].tolist(),
            'bollinger_low': hist['Bollinger Low'].tolist(),
            'rsi': hist['RSI'].tolist(),
            'macd': hist['MACD'].tolist(),
            'signal_line': hist['Signal Line'].tolist()
        }

    return render(request, 'mum_grafik.html',
                  {'data': data, 'sembol': sembol, 'period': period, 'window': window, 'std_dev': std_dev,
                   'rsi_window': rsi_window, 'short_window': short_window, 'long_window': long_window,
                   'signal_window': signal_window})


def fetch_data(request):
    sembol = request.GET.get('sembol', None)
    period = request.GET.get('period', '1y')  # Varsayılan 1 yıl
    interval = '1d'  # Varsayılan günlük
    window = int(request.GET.get('window', 20))
    std_dev = int(request.GET.get('std_dev', 2))
    rsi_window = int(request.GET.get('rsi_window', 14))
    short_window = int(request.GET.get('short_window', 12))
    long_window = int(request.GET.get('long_window', 26))
    signal_window = int(request.GET.get('signal_window', 9))

    if period in ['1d', '5d']:
        interval = '1h'  # 1 günlük veya 5 günlük seçildiğinde saatlik
    elif period in ['1h', '4h', '8h']:
        interval = period  # 1 saat, 4 saat, 8 saat

    data = None

    if sembol:
        ticker = yf.Ticker(sembol)
        hist = ticker.history(period=period, interval=interval)  # Seçilen zaman periyoduna ve intervale göre veriyi çek
        hist = calculate_bollinger_bands(hist, window, std_dev)
        hist = calculate_rsi(hist, rsi_window)
        hist = calculate_macd(hist, short_window, long_window, signal_window)

        # NaN değerleri kaldırın
        hist = hist.dropna()

        data = {
            'dates': hist.index.strftime('%Y-%m-%d %H:%M:%S').tolist(),
            'open': hist['Open'].tolist(),
            'high': hist['High'].tolist(),
            'low': hist['Low'].tolist(),
            'close': hist['Close'].tolist(),
            'volume': hist['Volume'].tolist(),
            'bollinger_middle': hist['Bollinger Middle'].tolist(),
            'bollinger_high': hist['Bollinger High'].tolist(),
            'bollinger_low': hist['Bollinger Low'].tolist(),
            'rsi': hist['RSI'].tolist(),
            'macd': hist['MACD'].tolist(),
            'signal_line': hist['Signal Line'].tolist()
        }

    return JsonResponse(data)


def settings_view(request):
    if request.method == 'POST':
        form = SettingsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        form = SettingsForm()
    settings = Settings.objects.all()
    return render(request, 'settings.html', {'form': form, 'settings': settings})


def edit_setting(request, pk):
    setting = get_object_or_404(Settings, pk=pk)
    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=setting)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        form = SettingsForm(instance=setting)
    return render(request, 'edit_setting.html', {'form': form})


def download_file(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, 'stock_excel_files', filename)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
