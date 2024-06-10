import requests
from bs4 import BeautifulSoup
import pandas as pd


def stock_list():
    global columns
    url = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/default.aspx"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    # XPath ile div'i bul
    div = soup.select_one('#content > div > div:nth-of-type(3)')
    if div is None:
        print("Belirtilen div bulunamadı.")
        exit()
    # Div içindeki tabloyu bul
    table = div.find("table")
    if table is None:
        print("Tablo bulunamadı.")
        exit()
    # Verileri depolamak için listeler
    columns = []
    data = []
    # Sütun adlarını al
    headers = table.find_all("th")
    for header in headers:
        columns.append(header.text.strip())
    # Satırları al
    rows = table.find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        cell_data = [cell.text.strip() for cell in cells]
        if cell_data:
            data.append(cell_data)
    # DataFrame oluştur ve CSV'ye kaydet
    df = pd.DataFrame(data, columns=columns)
    df.to_csv("stocks.csv", index=False)
    print("Veriler başarıyla çekildi ve stocks.csv dosyasına kaydedildi.")



