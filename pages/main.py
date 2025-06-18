import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import yfinance as yf


st.set_page_config(
    page_title="Котировки акций",
    page_icon="📈",
    layout="centered"
)

# 0. Называем приложение и описываем его.

st.title('Мое первое приложение в мире DataScience')
st.write('''#### С помощью него вы можете посмотреть катировки акций различных компаний''')

st.write(f'''
## Ниже подробная таблица котировок, простые графики отображения цен и объема проданных акций различных компаний
''')

all_nasdaq = pd.read_csv('nasdaq_screener.csv')[['Symbol', 'Name']]
# st.dataframe(all_nasdaq)

selected_company = st.selectbox('Выбери компанию', all_nasdaq['Name'].values)
stock_ticker = all_nasdaq[all_nasdaq['Name'] == selected_company].reset_index(drop=True).loc[0, 'Symbol']

st.write(f'''Тикер данной компании на бирже: **{stock_ticker}**''')

stock_ticker_data = pd.DataFrame(yf.Ticker(stock_ticker).history(period='1d', start='2024-1-01', end='2024-12-31'))

if len(stock_ticker_data) == 0:
    st.write('''***К сожалению, тикер данной компании еще не обрабатывается платформой. Попробуйте выбрать другой вариант***''')
    st.stop()


# Подготавливаем dataset для таблицы
stock_ticker_data_copy = stock_ticker_data.reset_index()
stock_ticker_data_copy['Date'] = stock_ticker_data_copy['Date'].dt.date
stock_ticker_data_copy = stock_ticker_data_copy.set_index('Date')
stock_ticker_data_copy = stock_ticker_data_copy[['Open', 'High', 'Close', 'Volume']]
stock_ticker_data_copy['Volume'] = stock_ticker_data_copy['Volume'].map(lambda x: f'{x:,} stocks')
stock_ticker_data_copy['Open'] = stock_ticker_data_copy['Open'].map(lambda x: f'$ {x:,.2f}')
stock_ticker_data_copy['High'] = stock_ticker_data_copy['High'].map(lambda x: f'$ {x:,.2f}')
stock_ticker_data_copy['Close'] = stock_ticker_data_copy['Close'].map(lambda x: f'$ {x:,.2f}')


st.write(f'''
### 1. Ниже вы можете наблюдать котировки в таблице и подробно посмотреть необходимые данные по компании {selected_company}
''')
st.dataframe(stock_ticker_data_copy)

st.write(f""" 
### На графике ниже вы можете наблюдать изменение цены акций {selected_company} в 2024 году
 """)
st.line_chart(stock_ticker_data.Close)


st.write(f""" 
### На графике ниже вы можете наблюдать изменение объема проданных акций {selected_company} в 2024 году
 """)
st.line_chart(stock_ticker_data.Volume)


