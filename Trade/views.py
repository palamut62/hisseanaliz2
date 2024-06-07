from django.shortcuts import render, redirect
from Trade.forms import StockForm, AddStockForm
from Trade.models import Hisse
import yfinance as yf

from utils import hisse_bilgilerini_analiz_et


def index(request):
    stocks = Hisse.objects.all()
    summary_data = None
    hisse_bilgisi = None
    selected_stock = None
    google_gemini_degerlendirme=None
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

    if selected_stock:
        ticker = yf.Ticker(selected_stock)
        info = ticker.info
        hisse_bilgisi = {
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
            'address1': info.get('address1', 'N/A'),
            'address2': info.get('address2', 'N/A'),
            'city': info.get('city', 'N/A'),
            'zip': info.get('zip', 'N/A'),
            'country': info.get('country', 'N/A'),
            'phone': info.get('phone', 'N/A'),
            'fax': info.get('fax', 'N/A'),
            'website': info.get('website', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'fullTimeEmployees': info.get('fullTimeEmployees', 'N/A'),
            'longBusinessSummary': info.get('longBusinessSummary', 'N/A'),
        }
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



    return render(request, 'index.html', {
        'form': form,
        'add_stock_form': add_stock_form,
        'stocks': stocks,
        'summary_data': summary_data,
        'hisse_bilgisi': hisse_bilgisi,
        'selected_stock': selected_stock,
        'google_gemini_degerlendirme': google_gemini_degerlendirme
    })
