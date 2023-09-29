import json


class PortfolioManager:
    def __init__(self, filename="persistance/portfolio.json"):
        self.filename = filename
        # Load current portfolio to determine the next ID
        current_portfolio = self._load_portfolio()
        if any(stock["transactions"] for stock in current_portfolio["stocks"]):
            # Start the next ID from the highest ID in the portfolio + 1
            self.next_id = (
                max(
                    transaction["id"]
                    for stock in current_portfolio["stocks"]
                    for transaction in stock["transactions"]
                )
                + 1
            )
        else:
            # If there are no transactions, start the ID from 1
            self.next_id = 1

    def _load_portfolio(self):
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"stocks": []}

    def _save_portfolio(self, portfolio):
        with open(self.filename, "w") as f:
            json.dump(portfolio, f, indent=4)

    def add_stock(self, ticker, shares, price):
        ticker = ticker.upper()
        portfolio = self._load_portfolio()
        # Check if ticker already exists
        for stock in portfolio["stocks"]:
            if stock["ticker"] == ticker:
                stock["transactions"].append(
                    {"id": self.next_id, "shares": shares, "price": price}
                )
                break
        else:
            # If ticker doesn't exist, create a new entry
            portfolio["stocks"].append(
                {
                    "ticker": ticker,
                    "transactions": [
                        {"id": self.next_id, "shares": shares, "price": price}
                    ],
                }
            )
        # Increment the ID counter for the next stock addition
        self.next_id += 1
        self._save_portfolio(portfolio)

    def remove_stock(self, ticker):
        portfolio = self._load_portfolio()
        portfolio["stocks"] = [
            stock for stock in portfolio["stocks"] if stock["ticker"] != ticker
        ]
        self._save_portfolio(portfolio)

    def sell_stock(self, ticker, shares, method="LIFO"):
        portfolio = self._load_portfolio()
        for stock in portfolio["stocks"]:
            if stock["ticker"] == ticker:
                if method == "LIFO":
                    stock["transactions"].sort(key=lambda x: x["id"], reverse=True)
                else:  # FIFO
                    stock["transactions"].sort(key=lambda x: x["id"])

                shares_to_sell = shares
                while shares_to_sell > 0 and stock["transactions"]:
                    transaction = stock["transactions"][0]
                    if transaction["shares"] > shares_to_sell:
                        transaction["shares"] -= shares_to_sell
                        shares_to_sell = 0
                    else:
                        shares_to_sell -= transaction["shares"]
                        stock["transactions"].pop(0)

                # If no more transactions for this ticker, remove the ticker entry
                if not stock["transactions"]:
                    portfolio["stocks"].remove(stock)
                break

        self._save_portfolio(portfolio)

    def get_portfolio(self):
        return self._load_portfolio()

    def view_stock(self, ticker):
        portfolio = self._load_portfolio()
        for stock in portfolio["stocks"]:
            print(stock["ticker"])
            if stock["ticker"] == ticker:
                return stock
        return None  # Return None if ticker not found in portfolio


if __name__ == "__main__":
    manager = PortfolioManager()
