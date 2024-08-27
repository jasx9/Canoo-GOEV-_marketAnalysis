import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_company_data(ticker_symbol):
    # Set up the headers for the HTTP request
    headers = {
        'User-Agent': ''
    }

    # URL for the summary page of the specified ticker symbol on Yahoo Finance
    url_basic = f'https://finance.yahoo.com/quote/{ticker_symbol}'

    # Send an HTTP request to the URL
    response = requests.get(url_basic, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract general_data company information
        try:
            company_name = soup.find('h1', class_='D(ib) Fz(18px)').text
            market_cap = soup.find('td', {'data-test': 'MARKET_CAP-value'}).text
            previous_close = soup.find('td', {'data-test': 'PREV_CLOSE-value'}).text
            volume = soup.find('td', {'data-test': 'TD_VOLUME-value'}).text
            # print(company_name,market_cap,previous_close,volume)

            # # Extract return on investment data
            # roa = soup.find('span', string='Return on Assets (ttm)').find_next('td').text
            # roe = soup.find('span', string='Return on Equity (ttm)').find_next('td').text

            # Create a dictionary to store the extracted information
            company_data = {
                'Company Name': company_name,
                'Market Cap': market_cap,
                'Previous Close': previous_close,
                'Volume': volume,
                # '52-Week Change': fifty_two_week_change,
                # 'Return on Assets (ROA)': roa,
                # 'Return on Equity (ROE)': roe,
            }

            print(f"Company (General) data for {company_name} has been successfully retrieved.")

        except AttributeError as e:
            print(f"Failed to retrieve company (General) data. Error: {e}")
    else:
        print(f"Failed to retrieve (General) data. Status code: {response.status_code}")

    # Send an HTTP request to the URL
    response_returns = requests.get(url_basic + '/key-statistics', headers=headers)

    if response.status_code == 200:
        soup_returns = BeautifulSoup(response_returns.text, 'html.parser')

        try:
            raw_extract_statistics = []
            statistics = soup_returns.findAll('td', class_='Fw(500) Ta(end) Pstart(10px) Miw(60px)')
            # print(statistics)

            for stat in statistics:
                raw_extract_statistics.append(stat.text)
            # print(raw_extract_statistics)
            # print(raw_extract_statistics.index('-179.82%'))

            fifty_two_week_change = raw_extract_statistics[10]
            roa = raw_extract_statistics[42]
            roe = raw_extract_statistics[43]

            company_data['52-Week Change'] = fifty_two_week_change
            company_data['Return on Assets (ROA)'] = roa
            company_data['Return on Equity (ROE)'] = roe

            # Display and save the company data
            print(company_data)

            # Create a DataFrame from the dictionary
            df = pd.DataFrame([company_data])

            # Save the DataFrame to a CSV file
            df.to_csv(f"{ticker_symbol}_company_data.csv", index=False)

            print(f"Company (Return on Investment) data for {company_name} has been successfully retrieved.")

        except AttributeError as e:
            print(f"Failed to retrieve company (Return on Investment) data. Error: {e}")
    else:
        print(f"Failed to retrieve (Return on Investment) data. Status code: {response.status_code}")


# Example usage for Canoo (GOEV)
get_company_data("GOEV")
