import yfinance as yf

# Hisse senedi sembolünü belirtin
symbol = "AAPL"

# Ticker nesnesi oluşturun
ticker = yf.Ticker(symbol)

# Ticker sınıfının dökümantasyonunu görüntüleyin
help(ticker)