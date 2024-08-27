import requests
from bs4 import BeautifulSoup
import pandas as pd

GREENSTOCKNEWS_url = 'https://greenstocknews.com/stocks/electric-vehicle-stocks'
GSN_response = requests.get(url=GREENSTOCKNEWS_url)
GSN_soup = BeautifulSoup(GSN_response.text, 'html.parser')

GSN_ticker_span = GSN_soup.select('span.stock-symbol')
ticker_symbols = [val.text for val in GSN_ticker_span]

headers = {'User-Agent': ''}

info_list = []

for ticker_symbol in ticker_symbols:
    YF_response = requests.get(url=f'https://finance.yahoo.com/quote/{ticker_symbol}', headers=headers)
    YF_soup = BeautifulSoup(YF_response.text, 'html.parser')

    try:
        company_name = YF_soup.find('h1', class_='D(ib) Fz(18px)').text
        previous_close = YF_soup.find('td', {'data-test': 'OPEN-value'}).text
        volume = YF_soup.find('td', {'data-test': 'TD_VOLUME-value'}).text
        market_cap = YF_soup.find('td', {'data-test': 'MARKET_CAP-value'}).text

        info_dict = {
            'Company (symbol)': company_name,
            'Previous_close': previous_close,
            'Volume': volume,
            'Market_cap': market_cap
        }

        info_list.append(info_dict)

        # print(company_name)
        # print(info_dict)

    except AttributeError as e:
        print(f"Failed to retrieve data for {ticker_symbol}. Error: {e}")

# Create a DataFrame from the list of dictionaries
df = pd.DataFrame(info_list)

# Save the DataFrame to a CSV file
df.to_csv("company_data.csv", index=False)