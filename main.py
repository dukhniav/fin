from api.yfin import get_news, get_current_price
from persistance.simple_dp import PortfolioManager

def main():
    print(get_current_price('msft'))

    manager = PortfolioManager()
    # Test the functions
    manager.add_stock("GOOGL", 3, 2800.0)

    stk = manager.view_stock('GOOGL')
    for x in stk['transactions']:
        print(x)
    # manager.view_portfolio()

if __name__ == '__main__':
    main()
