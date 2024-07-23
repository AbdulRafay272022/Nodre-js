from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd 

# Initialize Selenium WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

class text_to_be_non_empty_in_element(object):
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        try:
            element = driver.find_element(*self.locator)
            return element.text.strip() != ""
        except StaleElementReferenceException:
            return False

def get_product_details(link):
    try:
        driver.get(link)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'root')))
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'ProductPage')))
        WebDriverWait(driver, 30).until(
            text_to_be_non_empty_in_element(
                (By.CSS_SELECTOR, ".ProductActions-Section.ProductActions-Section_type_name h1")
            )
        )

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        main = soup.find('main', class_='ProductPage')
        product_detail = main.find('div', class_='ContentWrapper ProductPage-Wrapper')
        product_action = product_detail.find('article', class_='ProductActions')
        heading = product_action.find('section', class_='ProductActions-Section ProductActions-Section_type_name').h1.text
        print(heading)
        short_description = product_action.find('section', class_='ProductActions-Section ProductActions-Section_type_short').div.text
        price = product_action.find('div', class_='ProductActions-PriceWrapper').find('del',class_='ProductPrice-HighPrice').text 
        sizes = [size.text for size in product_action.find('div', class_='ProductConfigurableAttributes-SwatchList').find_all('span', 'Attribute-Value')]
        product_info = [info.text for info in main.find('dl', 'ProductInformation-Attributes').find_all('div', 'ProductAttributeValue')]
        return {
            'product_name': heading,
            'short_description': short_description,
            'price': price,
            'size_list': sizes,
            'product_details': product_info
        }
    except Exception as e:  
        print(f'Error retrieving product details for {link}: {e}')
        return None
try:
    url = 'https://zellbury.com'
    for i in range(7,9):
        driver.get(url + '/men/t-shirts-and-polos?page='+str(i))
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.ID, 'root')))
        product_links = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.ProductCard a'))
        )
        
        links = [link.get_attribute('href') for link in product_links]
        #print(links)
        products = []
        
        for link in links:
            product_details = get_product_details(link)
            if product_details:
                products.append(product_details)
        print(products)
        df=pd.DataFrame(products)
        
        print("====================================================================================")
        df.to_excel('Man/T-shirts-and-polos'+str(i)+'.xlsx')
        print(f'Successful file number '+str(i))
except Exception as e:
    print(f'Error: {e}')
finally:
    driver.quit()
    