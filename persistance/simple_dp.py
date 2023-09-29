import json


class PortfolioManager:
    def __init__(
        self,
        portfolio_filename="persistance/portfolio.json",
        balance_filename="persistance/balances.json",
    ):
        self.portfolio_filename = portfolio_filename
        self.balance_filename = balance_filename

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
            with open(self.portfolio_filename, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"stocks": []}

    def _save_portfolio(self, portfolio):
        with open(self.portfolio_filename, "w") as f:
            json.dump(portfolio, f, indent=4)

    def _load_balance(self):
        try:
            with open(self.balance_filename, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"balance": 0.0}  # Default balance

    def _save_balance(self, balance_data):
        with open(self.balance_filename, "w") as f:
            json.dump(balance_data, f, indent=4)

    def view_balance(self):
        return self._load_balance()["balance"]

    def add_stock(self, ticker, shares, price):
        ticker = ticker.upper()
        portfolio = self._load_portfolio()

        # Check and update balance
        total_cost = shares * price
        balance_data = self._load_balance()
        if balance_data["balance"] < total_cost:
            raise ValueError("Insufficient funds to purchase stock.")
        balance_data["balance"] -= total_cost
        self._save_balance(balance_data)
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
        total_return = 0.0  # Tracks the total money returned from selling

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
                # Update balance after selling stocks
        balance_data = self._load_balance()
        balance_data["balance"] += total_return
        self._save_balance(balance_data)

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
