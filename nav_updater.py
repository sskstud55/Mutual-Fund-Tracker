import requests
import time

AMFI_API = "https://api.mfapi.in/mf/"

FUND_CODES = {
    'Canara Robeco Bluechip': '120503',
    'PGIM India Midcap': '125354',
    'Quant Small Cap': '120835'
}

def fetch_latest_nav():
    nav_data = {}
    for fund_name, scheme_code in FUND_CODES.items():
        response = requests.get(AMFI_API + scheme_code)
        if response.status_code == 200:
            latest_nav = response.json()['data'][0]['nav']
            nav_data[fund_name] = latest_nav
        else:
            nav_data[fund_name] = 'N/A'
    return nav_data

while True:
    nav_data = fetch_latest_nav()
    print("Updated NAV:", nav_data)
    time.sleep(43200) # Update every 12 hours
