# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 12:01:18 2024
@author: nikhil
"""
#############
## Transform the extracted data
#############

# Import required packages
import pandas as pd
from datetime import date
import requests

# Import required classes, methods and variables
from extract import ShopifyApi_NSS, get_orders_report, get_data, token


#############
# Transform Shopify data
#############

# Driver code
# Replace with your shop's domain, API key, and password
# Healthwick CA - SHOP 1
SHOP_URL = "{ADD_YOUR_SHOP_NAME_HERE}.myshopify.com"
API_KEY = "{ADD_YOUR_API_KEY}"
PASSWORD = "{ADD_YOUR_API_PASSWORD}"


shopify_nss_ca = ShopifyApi_NSS(SHOP_URL, API_KEY, PASSWORD)

orders_ca = shopify_nss_ca.get_shopify_orders()
orders_df_ca, lineitems_df_ca = shopify_nss_ca.orders_to_df(orders_ca)


orders_placed_today_ca, orders_placed_afternoon_ca = get_orders_report(
    orders_df_ca)

# Healthwick USA - SHOP 2

SHOP_URL = "{ADD_YOUR_SHOP_NAME_HERE}.myshopify.com"
API_KEY = "{ADD_YOUR_API_KEY}"
PASSWORD = "{ADD_YOUR_API_PASSWORD}"


shopify_nss_us = ShopifyApi_NSS(SHOP_URL, API_KEY, PASSWORD)

orders_us = shopify_nss_us.get_shopify_orders()
orders_df_us, lineitems_df_us = shopify_nss_us.orders_to_df(orders_us)


orders_placed_today_us, orders_placed_afternoon_us = get_orders_report(
    orders_df_us)


# Geri Fashions - SHOP 3

SHOP_URL = "{ADD_YOUR_SHOP_NAME_HERE}.myshopify.com"
API_KEY = "{ADD_YOUR_API_KEY}"
PASSWORD = "{ADD_YOUR_API_PASSWORD}"


shopify_nss_gf = ShopifyApi_NSS(SHOP_URL, API_KEY, PASSWORD)

orders_gf = shopify_nss_gf.get_shopify_orders()
orders_df_gf, lineitems_df_gf = shopify_nss_gf.orders_to_df(orders_gf)


orders_placed_today_gf, orders_placed_afternoon_gf = get_orders_report(
    orders_df_gf)

# Books for Business - SHOP 4

SHOP_URL = "{ADD_YOUR_SHOP_NAME_HERE}.myshopify.com"
API_KEY = "{ADD_YOUR_API_KEY}"
PASSWORD = "{ADD_YOUR_API_PASSWORD}"

shopify_nss_b4b = ShopifyApi_NSS(SHOP_URL, API_KEY, PASSWORD)

orders_b4b = shopify_nss_b4b.get_shopify_orders()
orders_df_b4b, lineitems_df_b4b = shopify_nss_b4b.orders_to_df(orders_b4b)


orders_placed_today_b4b, orders_placed_afternoon_b4b = get_orders_report(
    orders_df_b4b)
# net_unfulfilled_b4b = len(orders_df_b4b_f[orders_df_b4b_f['Fulfillment Status'] != 'fulfilled'])
net_unfulfilled_b4b = len(orders_df_b4b[orders_df_b4b['Fulfillment Status'].isna()])
pending_b4b = len(orders_df_b4b[(orders_df_b4b['Fulfillment Status'] != 'fulfilled') &
                            (orders_df_b4b['Tags'].str.contains('hold', case=False, na=False))])
shipped_b4b = len(orders_df_b4b[orders_df_b4b['Shipment Status'] == 'confirmed'])

print('Shopify data has been extracted and transformed successfully.')

#############
# Transform Fishbowl data
#############


#############
# Get unfulfilled from so
#############

# Fishbowl Server url
server_url = "{ADD_YOUR_FISHBOWL_SERVER_URL}"

# SQL QUERY
# query to get all sales orders / unfulfilled
unfulfilled_query = 'SELECT id,num,statusId FROM so WHERE statusId IN (20,25);'

# call function to get all sales orders / unfulfilled
total_unfulfilled = get_data(token, unfulfilled_query)

# filter to get unfulfilled - HW CA
unfd_hwca = len([d for d in total_unfulfilled if d['num'].startswith('20')])

# filter to get unfulfilled - HW USA ------not required for now
# unfd_hwus = len([d for d in total_unfulfilled if d['num'].startswith('#') and not d['num'].startswith('#2021')])

# filter to get unfulfilled - Geri
unfd_geri = len([d for d in total_unfulfilled if d['num'].startswith('#2021')])

# filter to get unfulfilled - B4B ------not required for now
# unfd_b4b = len([d for d in total_unfulfilled if d['num'].endswith('-N')])

#############
# Get pending and partial from pick
#############

# SQL QUERY
pending_query = 'SELECT num,id,statusId FROM pick WHERE statusId=10;'

pending = get_data(token, pending_query)

pending_df = pd.DataFrame(pending)

pickitems_query = '''SELECT orderId,pickId,qty,statusId
                    FROM pickitem
                    WHERE statusId IN (5,6,10,11,20,30);'''

pickitems = get_data(token, pickitems_query)

pickitems_df = pd.DataFrame(pickitems)

merged_df = pd.merge(pending_df, pickitems_df,
                     left_on='id', right_on='pickId',
                     suffixes=('_pending', '_pickitems'))


def determine_pick_status(status_ids):
    if any(status == 5 for status in status_ids) and any(status == 10 for status in status_ids):
        return 'Atleast one item is pickable'
    elif all(status == 5 for status in status_ids):
        return 'No items are pickable'
    elif all(status == 10 for status in status_ids):
        return 'All items are pickable'
    else:
        return 'Unknown'


# Group by 'id_pending' and aggregate to get statusId values
grouped = merged_df.groupby(
    'id')['statusId_pickitems'].apply(list).reset_index()

# Apply function to determine pick status
grouped['pick_status'] = grouped['statusId_pickitems'].apply(
    determine_pick_status)

pending_df = pd.merge(pending_df, grouped[['id', 'pick_status']], on='id')

total_pending = pending_df[(
    pending_df['pick_status'] != 'All items are pickable')]

pending_hwca = len(total_pending[total_pending['num'].str.startswith('S20')])

pending_geri = len(
    total_pending[total_pending['num'].str.startswith('S#2021')])

#############
# Get total shipped today
#############

today = date.today()

# SQL QUERY
shipped_query = f'''SELECT num,dateShipped,statusId FROM ship
                    WHERE statusId = 30
                    AND DATE(dateShipped)= '{today}';'''

shipped = pd.DataFrame(get_data(token, shipped_query))

shipped_hwca = len(shipped[shipped['num'].str.startswith('S20')])

shipped_geri = len(shipped[shipped['num'].str.startswith('S#2021')])

#############
# Logout
#############

logout_url = f"{server_url}/api/logout"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

response = requests.post(logout_url, headers=headers)

if response.status_code == 200:
    print('Logged out successfully')
else:
    print(f'{response.status_code}')
    print(f'{response.text}')

print('Fishbowl data has been extracted and transformed successfully.')