from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

import src.login_config as config
import pandas as pd

wait_time = 5
url = 'https://www.zoocasa.com/'

lst_of_listings_links = []

def selenium_start():
    """
    Open browser
    """
    options = Options()
    options.add_argument("--headless=new")

    browser = webdriver.Chrome(options=options)
    # browser = webdriver.Chrome()
    lst_of_listings_links = []
    browser.get(url)
    
    return browser
    
def first_time_login(browser):
    """
    First time login to determine whether we want to approach the Canadian or US version of the site
    """
    try:
        WebDriverWait(browser,wait_time).until(EC.element_to_be_clickable((By.XPATH,'//*[@class="style_choice__sLSfh"][position()=2]'))).click()
    except:
        pass
    
def login_credentials(browser):
    username, password = config.main()
    # login 
    # WebDriverWait(browser,wait_time).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="style_nav-btn__AHq2s"]'))).click()
    # Email
    email_login = WebDriverWait(browser,wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='loginRegistrationEmailTextField']")))
    email_login.send_keys(username)
    email_login.send_keys(Keys.ENTER)
    #Password
    pass_login = WebDriverWait(browser,wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='passwordLoginModal']")))
    pass_login.send_keys(password)
    pass_login.send_keys(Keys.ENTER)

def retrieve_sold_listings(browser, city, page):
    """
    Retrieve sold listings from one of the possible cities
    - ['richmond', 'burnaby', 'vancouver', 'delta','surrey', 'coquitlam']
    """ 
    
    sold_url = 'https://zoocasa.com/{}-bc-real-estate/sold?page={}'.format(city, page)
    browser.get(sold_url)
    browser.refresh()
    # If this "Sign in Required" shows up
    try:
        WebDriverWait(browser,wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-testid='overlaySignInBtn']"))).click()
        login_credentials(browser)
    except:
        pass

    try:
        WebDriverWait(browser,wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='closeListingModal']"))).click()
    except:
        pass
    
    try:
        WebDriverWait(browser,wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='overlaySignInBtn']"))).click()
        # WebDriverWait(browser,wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='overlayAcceptTermsMsg']"))).click()
        WebDriverWait(browser,wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='termsOfUseAcceptButton_31017']"))).click()
    except:
        pass    

    # Get href
    listings = WebDriverWait(browser,wait_time).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[class='style_street-address__TsB7y']")))
    print('# of listings = {}'.format(len(listings)))

    for listing in listings:
        # Find the <a> tag within the <p> tag
        a_tag = WebDriverWait(listing,10).until(EC.presence_of_element_located((By.XPATH, "./a")))
    
        # Get the value of the href attribute
        href_value = a_tag.get_attribute("href")
        # print(href_value)
        lst_of_listings_links.append(href_value)

    

def fn_to_retreive_sold_listings(browser, city, pages):
    for page in range(1,pages+1):
        print('Page number is {}'.format(page))
        retrieve_sold_listings(browser, city, page)
    
    browser.close()
    return lst_of_listings_links

def retreive_info(browser, dynamic_text):
    try:
        info = WebDriverWait(browser,wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, f"[data-testid='{dynamic_text}']")))
        return info.text
    except:
        return None

def retrieve_sell_info(browser, dynamic_text, inner_text):
    try:
        # Wait for all listing elements to be present
        listing_elements = WebDriverWait(browser, wait_time).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, f'.{dynamic_text}')))
        # print(listing_elements)
        
        for listing_element in listing_elements:
            # Find the listing status element within the listing element
            status_element = listing_element.find_element(By.CSS_SELECTOR, "[data-testid='listingStatus']")
            # Check if the status is "Sold"
            if status_element.text.strip().lower() == "sold":
                # Do something with the specific sold listing
                inner_elements  = WebDriverWait(listing_element, wait_time).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, f"[data-testid='{inner_text}']")))

                for element in inner_elements:
                    return element.text

    except Exception as e:
        return None

def retrieve_sold_listing_description(browser, url):
    """
    Retrieve sold listings descriptions from one of the possible cities
    - ['richmond', 'burnaby', 'vancouver', 'delta','surrey', 'coquitlam']
    """ 
    browser.get(url)
    first_time_login(browser)

    # If this "Sign in Required" shows up
    try:
        WebDriverWait(browser,wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='overlaySignInBtn']"))).click()
        login_credentials(browser)
        WebDriverWait(browser,wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='overlayAcceptTermsMsg']"))).click()
        WebDriverWait(browser,wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='termsOfUseAcceptButton_31017']"))).click()
    except:
        pass

    # Key Facts
    # TypeKeyFacts
    house_type = retreive_info(browser, 'TypeKeyFacts')
    size = retreive_info(browser, 'SizeKeyFacts')
    maint_fee = retreive_info(browser, 'MaintenanceFeesKeyFacts')
    approx_age = retreive_info(browser, 'Approx.AgeKeyFacts')
    mls_number = retreive_info(browser, 'MLS®NumberKeyFacts')
    levels = retreive_info(browser, 'LevelsKeyFacts')
    garage = retreive_info(browser, 'GarageKeyFacts')
    garage_size = retreive_info(browser, 'listingCarIcon')
    taxes = retreive_info(browser, 'TaxesKeyFacts')
    avg_price_sqft = retreive_info(browser, 'Avg.PricePerSqftKeyFacts')
    property_addr = retreive_info(browser, 'keyFactsPropertyAddress')
    bedroom = retreive_info(browser, 'listingBedIcon')
    bathroom = retreive_info(browser, 'listingBathIcon')

    list_date = retrieve_sell_info(browser, 'style_grid__CzhIW', 'priceHistoryRowDate')
    list_price = retrieve_sell_info(browser, 'style_grid__CzhIW', 'priceHistoryRowListPrice')
    end_date = retrieve_sell_info(browser, 'style_grid__CzhIW', 'priceHistoryRowSoldDate')
    sold_price = retrieve_sell_info(browser, 'style_grid__CzhIW', 'priceHistoryRowSoldPrice')
    

    df = pd.DataFrame({
        'house_type': [house_type],
        'size': [size],
        'maint_fee': [maint_fee],
        'approx_age': [approx_age],
        'mls_number': [mls_number],
        'levels': [levels],
        'garage': [garage],
        'garage_size': [garage_size],
        'taxes': [taxes],
        'avg_price_sqft': [avg_price_sqft],
        'property_addr': [property_addr],
        'bedroom': [bedroom],
        'bathroom': [bathroom],
        'list_date': [list_date],
        'list_price': [list_price],
        'end_date': [end_date],
        'sold_price': [sold_price]
}, index = [0])

    return df


