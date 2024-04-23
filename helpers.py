# helpers.py

import yfinance as yf
import pandas as pd
import cufflinks as cf

# ação -> data
def get_data(stock, period = "1y", interval = '1d'):
    return yf.download(stock, interval = interval, period = period, progress = False)

# data -> preço atual
def get_price(data):
    return f'{data["Close"].iloc[-1]:,.2f}'

# data -> mudança
def get_change(data):
    current_price = data["Close"].iloc[-1]
    last_price = data["Close"].iloc[-2]
    change = current_price - last_price
    return {
        'amount': f"${abs(change):.2f}",
        'percent': f"{change / last_price * 100:.2f}",
        'color': 'success' if change >= 0 else 'danger',
        'icon': 'arrow-up' if change >= 0 else 'arrow-down'
    }


def calcular_rentabilidade_acumulada(data):
    data['retorno_diario'] = data['Close'].pct_change()
    data = data.assign(retorno_acumulado = (((1 + data['retorno_diario']).cumprod()) - 1) * 100)
    return data['retorno_acumulado']


def get_acum(data):
    def calcular_rentabilidade_acumulada(data):
        data['retorno_diario'] = data['Close'].pct_change()
        data = data.assign(retorno_acumulado = (((1 + data['retorno_diario']).cumprod()) - 1) * 100)
        return data['retorno_acumulado']

    data_last_month = data.loc[(data.index >= data.index[-1] - pd.DateOffset(months=1)) & (data.index <= data.index[-1])]
    rentabilidade_last_month = calcular_rentabilidade_acumulada(data_last_month)[-1]

    data_last_3_months = data.loc[(data.index >= data.index[-1] - pd.DateOffset(months=3)) & (data.index <= data.index[-1])]
    rentabilidade_last_3_months = calcular_rentabilidade_acumulada(data_last_3_months)[-1]

    data_last_6_months = data.loc[(data.index >= data.index[-1] - pd.DateOffset(months=6)) & (data.index <= data.index[-1])]
    rentabilidade_last_6_months = calcular_rentabilidade_acumulada(data_last_6_months)[-1]

    data_last_12_months = data.loc[(data.index >= data.index[-1] - pd.DateOffset(months=12)) & (data.index <= data.index[-1])]
    rentabilidade_last_12_months = calcular_rentabilidade_acumulada(data_last_12_months)[-1]

    data_last_24_months = data.loc[(data.index >= data.index[-1] - pd.DateOffset(months=24)) & (data.index <= data.index[-1])]
    rentabilidade_last_24_months = calcular_rentabilidade_acumulada(data_last_24_months)[-1]

    tabela_ultimos_meses = pd.DataFrame({
        'Período': ['Último Mês', 'Últimos 3 Meses', 'Últimos 6 Meses', 'Últimos 12 Meses', 'Últimos 24 Meses'],
        'Rentabilidade Acumulada (%)': [rentabilidade_last_month, rentabilidade_last_3_months,
                                     rentabilidade_last_6_months, rentabilidade_last_12_months,
                                     rentabilidade_last_24_months]
    })

    return tabela_ultimos_meses.round(2)

# data -> tabela OHLC
def make_OHLC_table(data):
    return {
        'date': data.reset_index()['Date'].iloc[-1].date().strftime('%Y-%m-%d'),
        'open': f"${data['Open'].iloc[-1]:.2f}",
        'high': f"${data['High'].iloc[-1]:.2f}",
        'low': f"${data['Low'].iloc[-1]:.2f}",
        'close': f"${data['Close'].iloc[-1]:.2f}",
        'volume': f"{data['Volume'].iloc[-1]:,.0f}"
    }

# data -> gráfico candlestick
def make_candlestick_chart(data, ticker):
    cf.go_offline()
    qf=cf.QuantFig(data, legend='top', name=ticker)
    qf.add_sma([10,20],width=2,color=['green','lightgreen'],legendgroup=True)
    qf.add_rsi(periods=20,color='java')
    qf.add_bollinger_bands(periods=20,boll_std=2,colors=['magenta','grey'],fill=True)
    qf.add_volume()
    qf.add_macd()
    return qf.iplot()