import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, redirect, url_for, flash
from backend.api.yfin import get_current_price
from backend.persistance.simple_dp import PortfolioManager

app = Flask(__name__)
app.secret_key = "supersecretkey"  # For flash messages

manager = PortfolioManager()

@app.route('/')
def index():
    portfolio = manager.get_portfolio()
    balance = manager.view_balance()
    return render_template('/index.html', portfolio=portfolio, balance=balance)

@app.route('/buy_stock', methods=['POST'])
def buy_stock():
    ticker = request.form['ticker'].upper()
    shares = int(request.form['shares'])
    price = get_current_price(ticker)
    try:
        manager.add_stock(ticker, shares, price)
        flash(f'Successfully purchased {shares} shares of {ticker}', 'success')
    except ValueError as e:
        flash(str(e), 'error')
    return redirect(url_for('index'))

@app.route('/sell_stock', methods=['POST'])
def sell_stock():
    ticker = request.form['ticker'].upper()
    shares = int(request.form['shares'])
    method = request.form.get('method', 'LIFO').upper()
    manager.sell_stock(ticker, shares, method)
    flash(f'Successfully sold {shares} shares of {ticker} using {method} method', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
