from selenium import webdriver  # allow launching browser
from selenium.webdriver.common.by import By  # allow search with parameters
from selenium.webdriver.support.ui import WebDriverWait # allow waiting for page to load
from selenium.webdriver.support import expected_conditions as EC # determine whether the web page has loaded
from selenium.common.exceptions import TimeoutException  # handling timeout situation
import pandas as pd

driver_option = webdriver.ChromeOptions()
driver_option.add_argument(" — incognito")

# Change this to your own chromedriver path!
chromedriver_path = '/Users/Korisnik/Downloads/Code/chromedriver/chromedriver'

def create_webdriver():
    return webdriver.Chrome(executable_path=chromedriver_path, chrome_options=driver_option)

browser = create_webdriver()
browser.get("") #Page you wish to scrap

i = 0

# Extract all products
# "//h1[@class='h3 lh-condensed']"
products = browser.find_elements(By.XPATH, ("//div[@class='product-right-side clear']"))

# Extract information for each project
product_list = {}
for prod in products:

    prod_name = prod.find_elements(By.XPATH, ("//h4[@itemprop='name']"))[i].get_attribute("innerHTML")
    prod_price = prod.find_elements(By.XPATH, ("//span[@class='ppra_price-number snowflake']"))[i].get_attribute("innerHTML")
    prod_url = prod.find_elements(By.XPATH, ("//a[@class='product-item-name']"))[i].get_attribute('href')

    product_list[prod_url] = prod_name, prod_price
    i += 1

# Close connection
browser.quit()

# Extracting data
product_df = pd.DataFrame.from_dict(product_list, orient='index')

# Manipulate the table
product_df['product_name'] = product_df.index
product_df.columns = ['product_name', 'price', 'url']
product_df = product_df.reset_index(drop=True)

# Export project dataframe to CSV
product_df.to_csv('product_list.csv')
