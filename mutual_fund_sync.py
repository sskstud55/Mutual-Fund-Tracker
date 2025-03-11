import requests

GROWW_API = "https://groww.in/api/v2/portfolio"

headers = {
    'Authorization': 'Bearer <access_token>',
    'Content-Type': 'application/json'
}

def fetch_portfolio():
    response = requests.get(GROWW_API, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def calculate_total_value(data):
    total_value = 0
    for fund in data['funds']:
        total_value += fund['current_value']
    return total_value

portfolio_data = fetch_portfolio()
if portfolio_data:
    print("Total Portfolio Value: ₹", calculate_total_value(portfolio_data))
else:
    print("Failed to fetch data.")
