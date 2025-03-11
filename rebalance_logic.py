import requests

THRESHOLD_PROFIT = 30
THRESHOLD_LOSS = -10

def fetch_portfolio():
    # Assuming data is already fetched via mutual_fund_sync.py
    # Mock Data:
    return [
        {"name": "Canara Robeco Bluechip", "invested": 250000, "current_value": 375000},
        {"name": "Quant Small Cap", "invested": 88000, "current_value": 102000}
    ]

def calculate_profit_loss(fund):
    invested = fund['invested']
    current_value = fund['current_value']
    return ((current_value - invested) / invested) * 100

def trigger_rebalance():
    portfolio = fetch_portfolio()
    for fund in portfolio:
        profit = calculate_profit_loss(fund)
        if profit >= THRESHOLD_PROFIT:
            print(f"✅ Book Profit in {fund['name']} - Profit: {profit:.2f}%")
        elif profit <= THRESHOLD_LOSS:
            print(f"❌ Deploy More Capital in {fund['name']} - Loss: {profit:.2f}%")

trigger_rebalance()
