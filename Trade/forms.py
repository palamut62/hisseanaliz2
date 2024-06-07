from django import forms
from Trade.models import Hisse
import yfinance as yf


class StockForm(forms.Form):
    symbol = forms.ChoiceField(label='Hisse Seç', required=True)


    def __init__(self, *args, **kwargs):
        super(StockForm, self).__init__(*args, **kwargs)
        hisse_choices = [(hisse.sembol, hisse.isim) for hisse in Hisse.objects.all()]
        self.fields['symbol'].choices = hisse_choices

        # Form gönderilmişse, seçilen hisseyi önceden doldur
        if 'symbol' in self.data:
            try:
                initial_symbol = self.data['symbol']
                self.fields['symbol'].initial = initial_symbol
            except KeyError:
                pass


class AddStockForm(forms.ModelForm):
    class Meta:
        model = Hisse
        fields = ['sembol', 'isim']
        labels = {
            'sembol': 'Sembol',
            'isim': 'İsim',
        }


