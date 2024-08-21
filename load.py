# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 12:01:18 2024
@author: nikhil
"""
#############
## Load to NSS Report - Google Sheets
#############

# import required packages
import gspread
from google.oauth2.service_account import Credentials

#import transformed variables
from transform import (orders_placed_today_us, 
                     orders_placed_afternoon_us,
                     orders_placed_today_ca,
                     orders_placed_afternoon_ca,
                     orders_placed_today_gf,
                     orders_placed_afternoon_gf,
                     net_unfulfilled_b4b,
                     pending_b4b,
                     shipped_b4b,
                     orders_placed_today_b4b,
                     orders_placed_afternoon_b4b,
                     unfd_hwca,
                     pending_hwca,
                     shipped_hwca,
                     unfd_geri,
                     pending_geri,
                     shipped_geri)

#############
# Load Shopify data
#############

# Path to your Service Account credentials file
creds_file = '{ADD_YOUR_SERVICE_ACCOUNT_CREDENTIAL_FILE_PATH_FROM_GOOGLE_CLOUD_CONSOLE}'

# Define the scope for the credentials
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

# Authorize the credentials
creds = Credentials.from_service_account_file(creds_file, scopes=scope)
client = gspread.authorize(creds)

# Open the Google Sheet by its name
spreadsheet = client.open('NSS Report Template')

# Select the specific sheet by name
sheet = spreadsheet.worksheet('NSS')

# Write data to specific cells
# Orders placed today
# HW US
sheet.update_acell('C9', str(orders_placed_today_us))
sheet.update_acell('C10', str(orders_placed_afternoon_us))

# HW CA
sheet.update_acell('D9', str(orders_placed_today_ca))
sheet.update_acell('D10', str(orders_placed_afternoon_ca))

# GF
sheet.update_acell('E9', str(orders_placed_today_gf))
sheet.update_acell('E10', str(orders_placed_afternoon_gf))

# B4B
# B4B Pending and Unfulfilled
sheet.update_acell('F5', str(net_unfulfilled_b4b))
sheet.update_acell('F6', str(pending_b4b))
sheet.update_acell('F8', str(shipped_b4b))
sheet.update_acell('F9', str(orders_placed_today_b4b))
sheet.update_acell('F10', str(orders_placed_afternoon_b4b))

print('Shopify data has been loaded to the sheet successfully.')


#############
# Load Fishbowl data
#############

# HW CA
sheet.update_acell('D5', str(unfd_hwca))
sheet.update_acell('D6', str(pending_hwca))
sheet.update_acell('D8', str(shipped_hwca))

# GF
sheet.update_acell('E5', str(unfd_geri))
sheet.update_acell('E6', str(pending_geri))
sheet.update_acell('E8', str(shipped_geri))

print('Fishbowl data has been loaded to the sheet successfully.')