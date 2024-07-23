from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

# Initialize Selenium WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
product=[]
'''try:
    pro_dict={}
    # Open the webpage
    driver.get('https://zellbury.com/embroidered-kurta-dupatta-trouser-yellow-lawn-1765')

    try:
        # Wait for the main content to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'root'))
        )
    except TimeoutException:
        raise ValueError('Page not found or took too long to load')    

    # You can directly access elements with Selenium if needed
    # For example, waiting for a specific element to be loaded
    main_content = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'ProductPage'))
    )

    
    # Or, parse the entire page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Now, use BeautifulSoup to find elements
    #div = soup.find('div', id='root')
    main = soup.find('main', class_='ProductPage')
    product_detail = main.find('div', class_='ContentWrapper ProductPage-Wrapper')
    product_action=product_detail.find('article',class_='ProductActions')
    heading=product_action.find('section',class_='ProductActions-Section ProductActions-Section_type_name').h1.text
    #sku=product_action.find('section',class_='ProductActions-Section ProductActions-Section_type_sku').find('span',class_='ProductActions-Sku')
    short=product_action.find('section',class_='ProductActions-Section ProductActions-Section_type_short').find('div',class_='ProductActions-ShortDescription').div.text
    price=product_action.find('div',class_='ProductActions-PriceWrapper').find('del',class_='ProductPrice-HighPrice').text  
    sizes=product_action.find('div',class_='ProductConfigurableAttributes-SwatchList').find_all('div','SizeAttributes-Values')
    size_list=[]
    #print(sizes,len(sizes))
    for size in sizes:
        size_li=size.find_all('span','Attribute-Value')
        if size_li:
            for i in range(1,len(size_li)):
                size_list.append(size_li[i].text)
    
    product_info=main.find('dl','ProductInformation-Attributes')
    product_info_list=product_info.find_all('div','ProductAttributeValue')
    product_final_info=[]
    for pro in product_info_list:
        product_final_info.append(pro.text)
    #print(size_list)                                                                                                                           
    #print(heading,short,price,size_list)
    #print(product_final_info)
    pro_dict={'product_name':heading,'short_description':short,'price':price,'size_list':size_list,'product_details':product_final_info}
    product.append(pro_dict)
except Exception as e:
    print(f'Error {e}')
finally:
    # Make sure to quit the driver to free resources
    driver.quit()
    print(product)'''
def get_product_details(link):
    try:
        driver.get(link)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'root')))
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'ProductPage')))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        main = soup.find('main', class_='ProductPage')
        product_detail = main.find('div', class_='ContentWrapper ProductPage-Wrapper')
        product_action = product_detail.find('article', class_='ProductActions')
        heading = product_action.find('section', class_='ProductActions-Section ProductActions-Section_type_name').h1.text
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
link='https://zellbury.com/embroidered-kurta-dupatta-trouser-yellow-lawn-1765'
pro=get_product_details(link)
print(pro)