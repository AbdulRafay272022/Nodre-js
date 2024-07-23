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
url='https://zellbury.com'
try:
    page_link=[]
    product=[]
    driver.get(url+'/women/ready-to-wear')
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.ID,'root')))
    except TimeoutException:
        raise ValueError('Page not found or took too long to load') 
    main_content = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.ProductListPage.CategoryProductList-Page'))#when have multiple classes
    )
    main_content = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.ProductCard a[href]'))#Presence means that the element is in the DOM of the page, which does not necessarily mean that the element is visible.
    )
    soup=BeautifulSoup(driver.page_source,'html.parser')   
    Product_Page=soup.find('ul',class_='ProductListPage CategoryProductList-Page')
    product_list_page=Product_Page.find_all('li',class_='ProductCard')
    print(len(product_list_page))
    for li in product_list_page:
        page_link.append(li.a['href'])
    #print(product_list_page)
    print(page_link)
    for link in page_link:
        
        try:
            pro_dict={}
            # Open the webpage
            #print(url+link)
            driver.get(url+link)
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
        

except Exception as e:
    print(f'Error: {e}')         
finally:
            # Make sure to quit the driver to free resources
    driver.quit()
    print(product)