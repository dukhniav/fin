import yfinance as yf

def check_exists(ticker):
    try:
        stock = yf.Ticker(ticker)
        return True
    except:
        return False
    
def get_historical_data(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date)
    return data


def get_realtime_data(ticker):
    stock = yf.Ticker(ticker)
    return stock.info


def get_dividends_and_splits(ticker):
    stock = yf.Ticker(ticker)
    dividends = stock.dividends
    splits = stock.splits
    return dividends, splits


def get_company_info(ticker):
    stock = yf.Ticker(ticker)
    return {
        "shortName": stock.info["shortName"],
        "longBusinessSummary": stock.info["longBusinessSummary"],
        "sector": stock.info["sector"],
        "industry": stock.info["industry"],
        "country": stock.info["country"],
    }


def get_financial_statements(ticker):
    stock = yf.Ticker(ticker)
    income_statement = stock.financials
    balance_sheet = stock.balance_sheet
    cash_flow = stock.cashflow
    return income_statement, balance_sheet, cash_flow


def get_financial_ratios(ticker):
    stock = yf.Ticker(ticker)
    return stock.info


def get_tickers_from_group():
    tickers = yf.Tickers("^GSPC")
    return [ticker for ticker in tickers.tickers]


def get_option_chain(ticker, date=None):
    stock = yf.Ticker(ticker)
    if date:
        return stock.option_chain(date)
    return stock.option_chain()


def get_news(ticker):
    stock = yf.Ticker(ticker)
    return stock.news


def get_current_price(ticker_symbol):
    # Fetch the latest data for the ticker
    ticker = yf.Ticker(ticker_symbol)

    # Get today's data
    today_data = ticker.history(period="1d")

    # Return the 'Close' price which represents the latest price
    return today_data["Close"].iloc[0]
