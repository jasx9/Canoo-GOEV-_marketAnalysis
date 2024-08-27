import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_financial_performance(ticker_symbol):
    # Set up the headers for the HTTP request
    headers = {
        'User-Agent': ''
    }
    financial_performance = {}

    # URL for the basic page of the specified ticker symbol on Yahoo Finance
    url_basic = f'https://finance.yahoo.com/quote/{ticker_symbol}'

    # Send an HTTP request to the URL modified to get income-statement.
    response_financials = requests.get(url_basic + '/financials', headers=headers)

    # Check if the request was successful (status code 200)
    if response_financials.status_code == 200:
        # Parse the HTML content of the page
        soup_financials = BeautifulSoup(response_financials.text, 'html.parser')

        try:
            # Extract income statement data
            raw_extract_financials = []
            income_statement = soup_financials.findAll('div', {'data-test': 'fin-col'})

            for element in income_statement:
                raw_extract_financials.append(element.text)
            # print(raw_extract_financials)

            total_revenue = raw_extract_financials[0] + ',000'
            cost_of_revenue = raw_extract_financials[4] + ',000'
            gross_profit = raw_extract_financials[8] + ',000'
            # print(type(total_revenue), type(cost_of_revenue), type(gross_profit))

            # Create a dictionary to store the extracted information
            financial_performance = {
                'Total Revenue': total_revenue,
                'Cost of Revenue': cost_of_revenue,
                'Gross Profit': gross_profit,
            }
            # print(financial_performance)

            print(f"Financial (Income Statement) data for {ticker_symbol} has been successfully retrieved.")
        except AttributeError as e:
            print(f"Failed to retrieve Financial (Income Statement) data. Error: {e}")
    else:
        print(f"Failed to retrieve data. Status code: {response_financials.status_code}")

    # Send an HTTP request to the URL modified to get balance-sheet.
    response_balance = requests.get(url_basic + '/balance-sheet', headers=headers)

    if response_balance.status_code == 200:
        soup_balance = BeautifulSoup(response_balance.text, 'html.parser')

        try:
            # Extract balance sheet data
            raw_extract_balance = []
            balance_sheet = soup_balance.findAll('div', {'data-test': 'fin-col'})

            for element in balance_sheet:
                raw_extract_balance.append(element.text)
            # print(raw_extract_balance)

            total_assets = raw_extract_balance[0] + ',000'
            total_liabilities = raw_extract_balance[3] + ',000'
            total_equity = raw_extract_balance[6] + ',000'

            # Updating Dictionary to store extracted information
            financial_performance['Total Assets'] = total_assets
            financial_performance['Total Liabilities'] = total_liabilities
            financial_performance['Total Equity'] = total_equity
            # print(financial_performance)

            print(f"Financial (Balance Sheet) data for {ticker_symbol} has been successfully retrieved.")
        except AttributeError as e:
            print(f"Failed to retrieve Financial (Balance Sheet) data. Error: {e}")
    else:
        print(f"Failed to retrieve data. Status code: {response_balance.status_code}")

    # Send an HTTP request to the URL modified to get Cash-flow.
    response_cash = requests.get(url_basic + '/cash-flow', headers=headers)

    # Check if the request was successful (status code 200)
    if response_cash.status_code == 200:
        soup_cash = BeautifulSoup(response_cash.text, 'html.parser')

        try:
            # Extract cash flow data
            raw_extract_cash = []
            balance_sheet = soup_cash.findAll('div', {'data-test': 'fin-col'})

            for element in balance_sheet:
                raw_extract_cash.append(element.text)
            # print(raw_extract_cash)

            # Extract expense structure data
            operating_cash_flow = raw_extract_cash[0] + ',000'
            investing_cash_flow = raw_extract_cash[4] + ',000'
            financing_cash_flow = raw_extract_cash[8] + ',000'
            end_cash_position = raw_extract_cash[12] + ',000'

            # Updating Dictionary to store extracted information
            financial_performance['Operating Cash Flow'] = operating_cash_flow
            financial_performance['Investing Cash Flow'] = investing_cash_flow
            financial_performance['Financing Cash Flow'] = financing_cash_flow
            financial_performance['End Cash Position'] = end_cash_position

            print(f"Financial (Cash Flow) data for {ticker_symbol} has been successfully retrieved.")
            # print(financial_performance)

            # Create a DataFrame from the dictionary
            df = pd.DataFrame([financial_performance])

            # Save the DataFrame to a CSV file
            df.to_csv("Canoo_financial_performance.csv", index=False)

        except AttributeError as e:
            print(f"Failed to retrieve Financial (Cash Flow) data. Error: {e}")

    else:
        print(f"Failed to retrieve data. Status code: {response_balance.status_code}")


# Example usage for Canoo (GOEV)
get_financial_performance("GOEV")
