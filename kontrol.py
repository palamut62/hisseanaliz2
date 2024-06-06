import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Şirketin hisse senedi sembolü
symbol = 'MIATK.IS'

# Hisse senedi bilgilerini al
stock = yf.Ticker(symbol)

# Finansal verileri al
financials = stock.financials
balance_sheet = stock.balance_sheet
cashflow = stock.cashflow
info = stock.info

# Gerekli finansal veriler
current_price = info['currentPrice']
market_cap = info['marketCap']
pe_ratio = info['trailingPE']
pb_ratio = info['priceToBook']

# Gelir tablosu ve bilanço verileri
income_statement = stock.financials.T
balance_sheet = stock.balance_sheet.T

# 2024 ve 2023 verileri
income_statement_2024 = income_statement.loc['2024']
income_statement_2023 = income_statement.loc['2023']

balance_sheet_2024 = balance_sheet.loc['2024']
balance_sheet_2023 = balance_sheet.loc['2023']

# Satışlar
sales_2024 = income_statement_2024['Total Revenue']
sales_2023 = income_statement_2023['Total Revenue']

# Brüt Kar
gross_profit_2024 = income_statement_2024['Gross Profit']
gross_profit_2023 = income_statement_2023['Gross Profit']

# FAVÖK
ebitda_2024 = income_statement_2024['Ebitda']
ebitda_2023 = income_statement_2023['Ebitda']

# Net Parasal Pozisyon Kazançları (Kayıpları)
net_monetary_position_2024 = income_statement_2024['Net Income']
net_monetary_position_2023 = income_statement_2023['Net Income']

# Net Dönem Karı
net_income_2024 = income_statement_2024['Net Income']
net_income_2023 = income_statement_2023['Net Income']

# Dönen Varlıklar
current_assets_2024 = balance_sheet_2024['Total Current Assets']
current_assets_2023 = balance_sheet_2023['Total Current Assets']

# Duran Varlıklar
non_current_assets_2024 = balance_sheet_2024['Total Non Current Assets']
non_current_assets_2023 = balance_sheet_2023['Total Non Current Assets']

# Toplam Varlıklar
total_assets_2024 = balance_sheet_2024['Total Assets']
total_assets_2023 = balance_sheet_2023['Total Assets']

# Net Borç
total_debt_2024 = balance_sheet_2024['Total Debt']
cash_and_cash_equivalents_2024 = balance_sheet_2024['Cash']
net_debt_2024 = total_debt_2024 - cash_and_cash_equivalents_2024

total_debt_2023 = balance_sheet_2023['Total Debt']
cash_and_cash_equivalents_2023 = balance_sheet_2023['Cash']
net_debt_2023 = total_debt_2023 - cash_and_cash_equivalents_2023

# Özsermaye
total_equity_2024 = balance_sheet_2024['Total Stockholder Equity']
total_equity_2023 = balance_sheet_2023['Total Stockholder Equity']

# Değerlerin yazdırılması
print(f"Hisse Fiyatı: {current_price} TL")
print(f"F/K Oranı: {pe_ratio}")
print(f"PD/DD Oranı: {pb_ratio}")
print(f"Piyasa Değeri: {market_cap} TL")
print(f"Satışlar (2024): {sales_2024} TL")
print(f"Satışlar (2023): {sales_2023} TL")
print(f"Brüt Kar (2024): {gross_profit_2024} TL")
print(f"Brüt Kar (2023): {gross_profit_2023} TL")
print(f"FAVÖK (2024): {ebitda_2024} TL")
print(f"FAVÖK (2023): {ebitda_2023} TL")
print(f"Net Parasal Pozisyon Kazançları/Kayıpları (2024): {net_monetary_position_2024} TL")
print(f"Net Parasal Pozisyon Kazançları/Kayıpları (2023): {net_monetary_position_2023} TL")
print(f"Net Dönem Karı (2024): {net_income_2024} TL")
print(f"Net Dönem Karı (2023): {net_income_2023} TL")
print(f"Dönen Varlıklar (2024): {current_assets_2024} TL")
print(f"Dönen Varlıklar (2023): {current_assets_2023} TL")
print(f"Duran Varlıklar (2024): {non_current_assets_2024} TL")
print(f"Duran Varlıklar (2023): {non_current_assets_2023} TL")
print(f"Toplam Varlıklar (2024): {total_assets_2024} TL")
print(f"Toplam Varlıklar (2023): {total_assets_2023} TL")
print(f"Net Borç (2024): {net_debt_2024} TL")
print(f"Net Borç (2023): {net_debt_2023} TL")
print(f"Özsermaye (2024): {total_equity_2024} TL")
print(f"Özsermaye (2023): {total_equity_2023} TL")

# Grafiklerin oluşturulması
years = ['2023', '2024']
sales = [sales_2023, sales_2024]
ebitda = [ebitda_2023, ebitda_2024]
net_income = [net_income_2023, net_income_2024]

fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 6))

axes[0].bar(years, sales, color=['purple', 'blue'])
axes[0].set_title('Yıllık Satışlar')
axes[0].set_ylabel('TL')

axes[1].bar(years, ebitda, color=['purple', 'blue'])
axes[1].set_title('Yıllık FAVÖK')
axes[1].set_ylabel('TL')

axes[2].bar(years, net_income, color=['purple', 'blue'])
axes[2].set_title('Yıllık Net Kar')
axes[2].set_ylabel('TL')

plt.tight_layout()
plt.show()
