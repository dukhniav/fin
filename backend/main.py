from persistance.simple_dp import PortfolioManager
from data_interface import DataInterface

def main():
    manager = PortfolioManager()
    di = DataInterface()

    while True:
        print("Menu:")
        print("1. Check current price of a stock")
        print("2. Buy stock")
        print("3. Sell stock")
        print("4. View balance")
        print("5. View portfolio")
        print("6. VIew performance statistics")
        print("7. View specific stock details in portfolio")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            ticker = input("Enter ticker symbol: ").upper()
            print(f"Current price of {ticker}: ${di.get_current_price(ticker):.2f}")

        elif choice == '2':
            ticker = input("Enter ticker symbol: ").upper()
            shares = int(input("Enter number of shares to buy: "))
            price = di.get_current_price(ticker)
            print(f"Buying {shares} shares of {ticker} at ${price:.2f} each")
            try:
                manager.add_stock(ticker, shares, price)
                print("Stock purchased successfully!")
            except ValueError as e:
                print(e)

        elif choice == '3':
            ticker = input("Enter ticker symbol: ").upper()
            shares = int(input("Enter number of shares to sell: "))
            method = input("Choose method (LIFO/FIFO): ").upper()
            print(f"Selling {shares} shares of {ticker}")
            manager.sell_stock(ticker, shares, method)
            print("Stock sold successfully!")

        elif choice == '4':
            print(f"Your current balance is: ${manager.view_balance():.2f}")

        # view portfolio
        elif choice == '5':
            portfolio = manager.get_portfolio()
            for stock in portfolio["stocks"]:
                print(stock["ticker"], "-", sum(transaction["shares"] for transaction in stock["transactions"]), "shares")

        # performance
        elif choice == '6':
            portfolio = manager.get_portfolio()
            for stock in portfolio["stocks"]:
                ticker = stock['ticker']
                cur_price = di.get_current_price(ticker)
                shares = sum(transaction['shares'] for transaction in stock['transactions'])
                print(f'{ticker} ({shares} @ ${cur_price}) - ${shares * cur_price}')

        elif choice == '7':
            ticker = input("Enter ticker symbol to view details: ").upper()
            stock_details = manager.view_stock(ticker)
            if stock_details:
                for x in stock_details['transactions']:
                    print(x)
            else:
                print(f"No details found for {ticker}")

        elif choice == '0':
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

        input("\nPress Enter to continue...")  # Wait for user to press enter

if __name__ == '__main__':
    main()
