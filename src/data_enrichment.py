import pandas as pd
from datetime import datetime
import re

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

def regex_cleanup(text):

    # Find the index of ":" and ","
    start_index = text.find(":")
    end_index = text.find(",")

    # Extract the text between ":" and ","
    if start_index != -1 and end_index != -1:
        extracted_text = text[start_index + 1:end_index].strip()
        return extracted_text
    else:
        return None

def geocode_json(address, city, gmaps):
    """
    Params: Address (text). Returns geocode json
    """
    text = address + ", " + city + ", british columbia, canada"
    try:
        geocode_result = gmaps.geocode(text)
        return geocode_result
    except:
        return None

def extract_geocode_postal(geocode_json):
    
    postal_code = None
    if geocode_json:
        if len(geocode_json) > 0 and 'address_components' in geocode_json[0]:
            for component in geocode_json[0]['address_components']:
                if 'postal_code' in component.get('types', []):
                    postal_code = component.get('long_name')
                    break
    return postal_code


def regex_fix_misc(dataframe):
    """
    Replace postal codes and address to correct format. These do not follow any rules and strictly manually searched on google.

    """
    dataframe.loc[dataframe['mls_number'] == 'R2818744','postal_code'] ='V5E 4M6'
    dataframe.loc[dataframe['mls_number'] == 'R2853587','postal_code'] ='V0V 0V0'
    dataframe.loc[dataframe['mls_number'] == 'R2591013','postal_code'] ='V3C 1E2'
    dataframe.loc[dataframe['mls_number'] == 'R2590096','postal_code'] ='V3J 5L9'
    dataframe.loc[dataframe['mls_number'] == 'R2853732','postal_code'] ='V4L' # 5
    dataframe.loc[dataframe['mls_number'] == 'R2587451','postal_code'] ='V4C 2X5' 
    dataframe.loc[dataframe['mls_number'] == 'R2577063','postal_code'] ='V4K 5E9' 
    dataframe.loc[dataframe['mls_number'] == 'R2578634','postal_code'] ='V4M 3N8' 
    dataframe.loc[dataframe['mls_number'] == 'R2582673','postal_code'] ='V4C 3G3' 
    
    dataframe.loc[dataframe['mls_number'] == 'R2866726','postal_code'] ='V6Y 4L9' 
    dataframe.loc[dataframe['mls_number'] == 'R2866726','address'] ='901 - 6333 Katsura Street' # fixing adddress while we're here
    
    dataframe.loc[dataframe['mls_number'] == 'R2811721','postal_code'] ='V7A 2S3' 
    dataframe.loc[dataframe['mls_number'] == 'R2811721','address'] ='9700 & 9720 Garden City Road' # fixing adddress while we're here
    
    dataframe.loc[dataframe['mls_number'] == 'R2584896','postal_code'] ='V7E 1K2' 
    
    dataframe.loc[dataframe['mls_number'] == 'R2579432','postal_code'] ='V3S 2V2' 
    dataframe.loc[dataframe['mls_number'] == 'R2579432','address'] ='16536 63 Avenue' # did not show up in original listing, google shows missing info
    
    dataframe.loc[dataframe['mls_number'] == 'R2585691','postal_code'] ='V4N 6V5' 
    dataframe.loc[dataframe['mls_number'] == 'R2585691','address'] ='17557 100 Avenue' # did not show up in original listing, google shows missing info
    
    dataframe.loc[dataframe['mls_number'] == 'R2596756','postal_code'] ='V3R 2C4' 
    dataframe.loc[dataframe['mls_number'] == 'R2596756','address'] ='14672 111 Avenue' # did not show up in original listing, google shows missing info
    
    dataframe.loc[dataframe['mls_number'] == 'R2593212','postal_code'] ='V3S 9V2' 
    dataframe.loc[dataframe['mls_number'] == 'R2593212','address'] ='16589 25 Avenue' # did not show up in original listing, google shows missing info
    
    dataframe.loc[dataframe['mls_number'] == 'R2594540','postal_code'] ='V3T 1X6' 
    dataframe.loc[dataframe['mls_number'] == 'R2594540','address'] ='14171 104 Avenue' # did not show up in original listing, google shows missing info
    
    dataframe.loc[dataframe['mls_number'] == 'R2561445','postal_code'] ='V4A 8K7' 
    dataframe.loc[dataframe['mls_number'] == 'R2561445','address'] ='12936 19 Avenue' # did not show up in original listing, google shows missing info
    
    dataframe.loc[dataframe['mls_number'] == 'R2595404','postal_code'] ='V3S 0G3' 
    dataframe.loc[dataframe['mls_number'] == 'R2595404','address'] ='15454 32 Avenue' # did not show up in original listing, google shows missing info
    
    dataframe.loc[dataframe['mls_number'] == 'R2594183','postal_code'] ='V4N 5R4' 
    dataframe.loc[dataframe['mls_number'] == 'R2594183','address'] ='17330 104 Avenue' # did not show up in original listing, google shows missing info

    dataframe.loc[dataframe['mls_number'] == 'R2592821','postal_code'] ='V4A 4N7' 
    dataframe.loc[dataframe['mls_number'] == 'R2592821','address'] ='15166 20 Avenue' # did not show up in original listing, google shows missing info
    
    dataframe.loc[dataframe['mls_number'] == 'R2745577','postal_code'] ='V3Z 0W4' 
    dataframe.loc[dataframe['mls_number'] == 'R2745577','address'] ='16760 25 Avenue' # did not show up in original listing, google shows missing info
    
    dataframe.loc[dataframe['mls_number'] == 'R2593212','postal_code'] ='V3S 9V2' 
    dataframe.loc[dataframe['mls_number'] == 'R2593212','address'] ='16589 25 Avenue' # did not show up in original listing, google shows missing info
    
    dataframe.loc[dataframe['mls_number'] == 'R2587546','postal_code'] ='V3S 7X3' 
    dataframe.loc[dataframe['mls_number'] == 'R2587546','address'] ='14940 62 Avenue' # did not show up in original listing, google shows missing info
    
    dataframe.loc[dataframe['mls_number'] == 'R2591498','postal_code'] ='V4A 1S7' 
    dataframe.loc[dataframe['mls_number'] == 'R2591498','address'] ='16228 16 Avenue' # did not show up in original listing, google shows missing info
    
    dataframe.loc[dataframe['mls_number'] == 'R2585891','postal_code'] ='V3Z 0J6' 
    dataframe.loc[dataframe['mls_number'] == 'R2585891','address'] ='15715 34 Avenue' # did not show up in original listing, google shows missing info
    
    dataframe.loc[dataframe['mls_number'] == 'R2593212','postal_code'] ='V3S 9V2' 
    dataframe.loc[dataframe['mls_number'] == 'R2593212','address'] ='16589 25 Avenue' # did not show up in original listing, google shows missing info
    
    dataframe.loc[dataframe['mls_number'] == 'R2584177','postal_code'] ='V3S 2N9' 
    dataframe.loc[dataframe['mls_number'] == 'R2584177','address'] ='18199 70 Avenue' # did not show up in original listing, google shows missing info
    
    dataframe.loc[dataframe['mls_number'] == 'R2586790','postal_code'] ='V3X 1Y8' 
    dataframe.loc[dataframe['mls_number'] == 'R2586790','address'] ='12038 62 Avenue' # did not show up in original listing, google shows missing info
    
    dataframe.loc[dataframe['mls_number'] == 'R2582146','postal_code'] ='V4A 5T3' 
    dataframe.loc[dataframe['mls_number'] == 'R2582146','address'] ='15420 22 Avenue' # did not show up in original listing, google shows missing info
    
    dataframe.loc[dataframe['mls_number'] == 'R2586656','postal_code'] ='V4A 1N7' 
    dataframe.loc[dataframe['mls_number'] == 'R2586656','address'] ='12926 16 Avenue' # did not show up in original listing, google shows missing info
    
    dataframe.loc[dataframe['mls_number'] == 'R2586150','postal_code'] ='V3R 0W8' 
    dataframe.loc[dataframe['mls_number'] == 'R2586150','address'] ='15258 105 Avenue' # did not show up in original listing, google shows missing info
    
    dataframe.loc[dataframe['mls_number'] == 'R2580364','postal_code'] ='V3R 2C1' 
    dataframe.loc[dataframe['mls_number'] == 'R2580364','address'] ='13711 111 Avenue' # did not show up in original listing, google shows missing info
    
    dataframe.loc[dataframe['mls_number'] == 'R2585691','postal_code'] ='V4N 6V5' 
    dataframe.loc[dataframe['mls_number'] == 'R2585691','address'] ='17557 100 Avenue' # did not show up in original listing, google shows missing info
    
    dataframe.loc[dataframe['mls_number'] == 'R2583651','postal_code'] ='V3S 9M9' 
    dataframe.loc[dataframe['mls_number'] == 'R2583651','address'] ='16565 20 Avenue' # did not show up in original listing, google shows missing info
    
    dataframe.loc[dataframe['mls_number'] == 'R2815446','postal_code'] ='V7W 2N5'
    dataframe.loc[dataframe['mls_number'] == 'R2831620','postal_code'] ='V5P 4X1'
    dataframe.loc[dataframe['mls_number'] == 'R2816348','postal_code'] ='V7M 0C8'
    dataframe.loc[dataframe['mls_number'] == 'R2797809','postal_code'] ='V7V 4R7'
    dataframe.loc[dataframe['mls_number'] == 'R2811638','postal_code'] ='V7M 1G7'

    dataframe.loc[dataframe['mls_number'] == 'R2793090','postal_code'] ='V7G 1M9'
    dataframe.loc[dataframe['mls_number'] == 'R2792117','postal_code'] ='V7R 1J8'
    dataframe.loc[dataframe['mls_number'] == 'R2811813','postal_code'] ='V7M 0C8'
    dataframe.loc[dataframe['mls_number'] == 'R2784735','postal_code'] ='V7V 2R2'
    dataframe.loc[dataframe['mls_number'] == 'R2810467','postal_code'] ='V7P 3E3'
    dataframe.loc[dataframe['mls_number'] == 'R2798338','postal_code'] ='V7P 3E3'
    dataframe.loc[dataframe['mls_number'] == 'R2806091','postal_code'] ='V5P 4X2'
    dataframe.loc[dataframe['mls_number'] == 'R2796849','postal_code'] ='V5P 4X5'
    dataframe.loc[dataframe['mls_number'] == 'R2805320','postal_code'] ='V7M 0E7'
    dataframe.loc[dataframe['mls_number'] == 'R2798035','postal_code'] ='V7M 0E4'
    dataframe.loc[dataframe['mls_number'] == 'R2787027','postal_code'] ='V7L 1G8'
    dataframe.loc[dataframe['mls_number'] == 'R2793128','postal_code'] ='V7P 3E3'
    dataframe.loc[dataframe['mls_number'] == 'R2795445','postal_code'] ='V7N 1T4'
    dataframe.loc[dataframe['mls_number'] == 'R2798427','postal_code'] ='V7P 3E3'
    dataframe.loc[dataframe['mls_number'] == 'R2800213','postal_code'] ='V7V 2P8'
    dataframe.loc[dataframe['mls_number'] == 'R2798099','postal_code'] ='V5P 4X2'
    dataframe.loc[dataframe['mls_number'] == 'R2795760','postal_code'] ='V7L 4Y1'
    
    dataframe.loc[dataframe['mls_number'] == 'R2793694','postal_code'] ='V7K 1V3'
    dataframe.loc[dataframe['mls_number'] == 'R2787000','postal_code'] ='V7P 3G7'
    dataframe.loc[dataframe['mls_number'] == 'R2789135','postal_code'] ='V0N 3Z1'
    dataframe.loc[dataframe['mls_number'] == 'R2781525','postal_code'] ='V7R 4N1'
    dataframe.loc[dataframe['mls_number'] == 'R2782166','postal_code'] ='V7R 1K8'
    dataframe.loc[dataframe['mls_number'] == 'R2777631','postal_code'] ='V7M 0E7'
    dataframe.loc[dataframe['mls_number'] == 'R2773284','postal_code'] ='V7W 1K3'
    dataframe.loc[dataframe['mls_number'] == 'R2772760','postal_code'] ='V7M 0C8'
    dataframe.loc[dataframe['mls_number'] == 'R2759288','postal_code'] ='V7L 1J9'
    dataframe.loc[dataframe['mls_number'] == 'R2757749','postal_code'] ='V7N 1M8'
    dataframe.loc[dataframe['mls_number'] == 'R2766456','postal_code'] ='V7W 1K4'
    dataframe.loc[dataframe['mls_number'] == 'R2765676','postal_code'] ='V7G 1V7'
    dataframe.loc[dataframe['mls_number'] == 'R2762608','postal_code'] ='V7R 1J9'
    dataframe.loc[dataframe['mls_number'] == 'R2763305','postal_code'] ='V7V 3Y1'
    dataframe.loc[dataframe['mls_number'] == 'R2747578','postal_code'] ='V7V 2R6'
    dataframe.loc[dataframe['mls_number'] == 'R2749954','postal_code'] ='V7N 1T5'
    dataframe.loc[dataframe['mls_number'] == 'R2747719','postal_code'] ='V7P 3G7'
    dataframe.loc[dataframe['mls_number'] == 'R2732940','postal_code'] ='V7K 1W4'
    dataframe.loc[dataframe['mls_number'] == 'R2733092','postal_code'] ='V7N 2H9'
    dataframe.loc[dataframe['mls_number'] == 'R2732402','postal_code'] ='V7M 1A2'
    dataframe.loc[dataframe['mls_number'] == 'R2732740','postal_code'] ='V7P 0B6'
    dataframe.loc[dataframe['mls_number'] == 'R2719441','postal_code'] ='V5W 2A4'
    dataframe.loc[dataframe['mls_number'] == 'R2680374','postal_code'] ='V5W 1J6'

    dataframe.loc[dataframe['mls_number'] == 'R2691911','postal_code'] ='V7L 4Y1'
    dataframe.loc[dataframe['mls_number'] == 'R2691273','postal_code'] ='V7L 4V1'
    dataframe.loc[dataframe['mls_number'] == 'R2697582','postal_code'] ='V7W 1Z3'
    dataframe.loc[dataframe['mls_number'] == 'R2694125','postal_code'] ='V7W 1K4'
    dataframe.loc[dataframe['mls_number'] == 'R2681196','postal_code'] ='V7G 1X5'
    dataframe.loc[dataframe['mls_number'] == 'R2678733','postal_code'] ='V7N 1T5'
    
    dataframe.loc[dataframe['mls_number'] == 'R2675473','postal_code'] ='V7M 3M8'
    dataframe.loc[dataframe['mls_number'] == 'R2672166','postal_code'] ='V7P 2V4'
    dataframe.loc[dataframe['mls_number'] == 'R2619813','postal_code'] ='V6B 2Y9'
    dataframe.loc[dataframe['mls_number'] == 'R2652439','postal_code'] ='V7P 3G7'
    dataframe.loc[dataframe['mls_number'] == 'R2646427','postal_code'] ='V0V 0V0'
    dataframe.loc[dataframe['mls_number'] == 'R2624525','postal_code'] ='V7L 1J9'
    dataframe.loc[dataframe['mls_number'] == 'R2638741','postal_code'] ='V7P 0B6'
    
    dataframe.loc[dataframe['mls_number'] == 'R2634806','postal_code'] ='V7P 3G7'
    dataframe.loc[dataframe['mls_number'] == 'R2627562','postal_code'] ='V7N 1T4'
    dataframe.loc[dataframe['mls_number'] == 'R2625903','postal_code'] ='V7J 3P7'
    dataframe.loc[dataframe['mls_number'] == 'R2617952','postal_code'] ='V7V 1K9'
    dataframe.loc[dataframe['mls_number'] == 'R2600345','postal_code'] ='V7S 3H5'
    dataframe.loc[dataframe['mls_number'] == 'R2618881','postal_code'] ='V7V 3Y1'
    dataframe.loc[dataframe['mls_number'] == 'R2618789','postal_code'] ='V7M 0E7'

    dataframe.loc[dataframe['mls_number'] == 'R2615877','postal_code'] ='V7M 0E4'
    dataframe.loc[dataframe['mls_number'] == 'R2606274','postal_code'] ='V7L 4X2'
    dataframe.loc[dataframe['mls_number'] == 'R2598098','postal_code'] ='V7L 1B2'
    dataframe.loc[dataframe['mls_number'] == 'R2602900','postal_code'] ='V7L 4X2'
    
    dataframe.loc[dataframe['mls_number'] == 'R2598975','postal_code'] ='V7W 1K2'
    dataframe.loc[dataframe['mls_number'] == 'R2573900','postal_code'] ='V7L 4X2'
    dataframe.loc[dataframe['mls_number'] == 'R2595920','postal_code'] ='V7S 3H5'
    dataframe.loc[dataframe['mls_number'] == 'R2596298','postal_code'] ='V7J 3B5'