import pandas as pd
from datetime import datetime

YEAR = 2024

def age_of_house(yr_house_built, year = YEAR):
    """
    Calculate the age of the house. By default, year is set to 2024.
    """
    try:
        return int(year - int(yr_house_built))
    except:
        return None

def calculate_days_to_sell(list_date, end_date):
    """
    Calculate the number of days it took for house listing to sell
    """
    try:
        listing_date = datetime.strptime(list_date, "%d/%m/%Y")
        sold_date = datetime.strptime(end_date, "%d/%m/%Y")
    
        days_difference = (sold_date - listing_date).days
        return days_difference
    except:
        return None

def calculate_price_diff_or_pct(list_price, sold_price, operation): 
    """
    Calculate the price difference or price percentage between the list price and sold price of a house listing.
    """
    try:
        # Check if list_price_str and sold_price_str are strings
        if not isinstance(list_price, str) or not isinstance(sold_price, str):
            raise ValueError("Input values are not strings")
        # Remove the dollar sign and commas, and convert strings to floats
        list_price = float(list_price.replace('$', '').replace(',', ''))
        sold_price = float(sold_price.replace('$', '').replace(',', ''))

        if operation == 'difference':
            result = sold_price - list_price
        elif operation == 'percentage':
            result = ((sold_price - list_price) / list_price) * 100
        else:
            raise ValueError("Invalid")
            
        return result
    except ValueError:
        return None