from api import yfin as yf 
from api import coingecko as cg

class DataInterface:
    def __init__(self) -> None:
        self.stock_data = yf
    
    def get_current_price(self, symbol):
        return self.stock_data.get_current_price(symbol)
