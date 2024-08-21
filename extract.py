# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 12:01:18 2024
@author: nikhil
"""

#############
## Extract data from different sources such as Shopify and Fishbowl inventory system
#############

# import packages
from datetime import date, time
import requests
import pandas as pd


#############
# SHOPIFY API
#############


class ShopifyApi_NSS:
    def __init__(self, shop_url, api_key, password):
        self.shop_url = shop_url
        self.api_key = api_key
        self.password = password
        self.api_version = '2024-01'

    def get_shopify_orders(self, limit=250):
        all_orders = []

        # Url with pagination by date
        orders_url = f"https://{self.shop_url}/admin/api/{self.api_version}/orders.json?status=any&limit={limit}"

        # Send API request to fetch orders data
        response = requests.get(orders_url, auth=(self.api_key, self.password))

        if response.status_code == 200:
            # If request successful, store it in a list
            orders_data = response.json().get('orders', [])

            # Populate all orders list
            all_orders.extend(orders_data)
        else:
            # If error, prints error and breaks runtime
            print(f"Error: {response.status_code} {response.text}")

        # Prints length of orders and returns orders and customer ids
        print(f"Total Orders: {self.shop_url} {len(all_orders)}")

        return all_orders

    def orders_to_df(self, orders):

        # List comprehensions to efficiently create order and line item data
        order_data = [
            {
                'Id': str(order.get('id')),
                'Created At': order.get('created_at'),
                'Total': float(order.get('current_total_price')),
                'Email': order.get('email'),
                'Financial Status': order.get('financial_status'),
                'Customer ID': str(order.get('customer').get('id')),
                'Source': order.get('source_name'),
                'Fulfillment Status': order.get('fulfillment_status'),
                'Tags': order.get('tags'),
                'Fulfillment At': order.get('fulfillments')[0].get('created_at') if order.get('fulfillments') else None,
                'Shipment Status': order.get('fulfillments')[0].get('shipment_status') if order.get('fulfillments') else None,
            } for order in orders
        ]

        lineitem_data = [
            {
                'Id': str(order.get('id')),
                'Created At':  order.get('created_at'),
                'Email': order.get('email'),
                'Financial Status': order.get('financial_status'),
                'Lineitem Title': item.get('title'),
                'Lineitem Price': float(item.get('price')),
                'Lineitem Quantity': int(item.get('quantity')),
                'Lineitem Vendor': item.get('vendor'),
                'SKU': item.get('sku'),
            }
            for order in orders
            for item in order.get('line_items')
        ]

        # Create dataframes
        order_df = pd.DataFrame(order_data)
        lineitem_df = pd.DataFrame(lineitem_data)

        # Type casting to split date & time
        for df in [order_df, lineitem_df]:
            df['Created At'] = pd.to_datetime(
                df['Created At']).dt.tz_localize(None)
            df['Date'] = df['Created At'].dt.date
            df['Time'] = df['Created At'].dt.time

        # Returns orders and lineitems dataframe
        return order_df, lineitem_df


def get_orders_report(orders_df):
    # Get orders placed today
    today = date.today()
    orders_today = orders_df[orders_df['Date'] == today]
    orders_placed_today = orders_today['Id'].count()

    # Get orders placed afternoon
    noon = time(12, 0, 0)
    orders_afternoon = orders_today[orders_today['Time'] >= noon]
    orders_placed_afternoon = orders_afternoon['Id'].count()

    return orders_placed_today, orders_placed_afternoon



#############
# FISHBOWL API
#############

#############
# Login
#############
server_url = "{ADD_YOUR_FISHBOWL_SERVER_URL}"


def fishbowl_login(server_url):
    login_url = f"{server_url}/api/login"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "appName": "API Integration",
        "appId": 108,
        "username": "{FISHBOWL_USERNAME}",
        "password": "{FISHBOWL_PASSWORD}!"
    }

    response = requests.post(login_url, headers=headers, json=data)

    if response.status_code == 200:
        print("Login successful")
        token = response.json()["token"]
        print(token)
        return token
    else:
        print("Login failed")
        print(response.status_code)
        print(response.text)
        return ""


token = fishbowl_login(server_url)

#############
# Get data function
#############


def get_data(token, query):
    data_url = f"{server_url}/api/data-query"

    headers = {
        "Content-Type": 'application/sql',
        "Authorization": f"Bearer {token}",
    }

    response = requests.get(data_url, headers=headers, data=query)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(response.status_code)
        print(response.text)
        return []























