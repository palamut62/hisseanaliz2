import os
import requests
from bs4 import BeautifulSoup
from isyatirimhisse import StockData, Financials
import pandas as pd
from tqdm import tqdm



def hisse_cek(data):
    financials = Financials()
    # Tüm hisselerin finansal verilerini çekip bir DataFrame'e kaydedin
    for hisse in tqdm(data, desc="Veriler indiriliyor"):
        try:
            finansal_veri = financials.get_data(symbols=hisse, exchange='TRY')
            df = pd.DataFrame(finansal_veri[hisse])  # Finansal veriyi DataFrame'e dönüştür

            # 'itemCode' ve 'itemDescEng' sütunlarını silin
            df.drop(columns=['itemCode', 'itemDescEng'], inplace=True)

            # Hisse sembolünü sütun olarak ekleyin
            df['Hisse Kodu'] = hisse

            # Hisse kodu sütununu silin
            df.drop(columns=['Hisse Kodu'], inplace=True)

            # Dosya yolunu belirtin
            kullanici_adi = os.getlogin()
            dosya_klasoru = "media/stock_excel_files/"

            # Klasör mevcut değilse oluştur
            if not os.path.exists(dosya_klasoru):
                os.makedirs(dosya_klasoru)

            # DataFrame'i CSV olarak kaydetme
            df.to_excel(os.path.join(dosya_klasoru, "{}.xlsx".format(hisse)), index=False)
        except KeyError:
            print(f"No data found for {hisse}. Skipping...")








