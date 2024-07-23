from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def scrape_page(session, url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.google.com/'  # sometimes setting a referrer helps
    }
    response = session.get(url, headers=headers)
    logger.info(f"URL: {url} - Status Code: {response.status_code}")
    
    if response.status_code != 200:
        logger.error(f"Failed to retrieve page {url}")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    page_content = soup.find(class_='page-content')
    
    if not page_content:
        logger.error(f"No page content found for {url}")
        return []

    data = []
    for link in page_content.find_all('a', class_='single-company-link'):
        href = link.get('href')
        data.append(href)
    
    logger.info(f"Found {len(data)} links")
    return data

def page(url, retries=3):
    logger.info(f"Processing URL: {url}")
    
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensure GUI is off
    
    driver = None  # Initialize driver variable
    for attempt in range(retries):
        try:
            # Set up the driver
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            
            # Open the URL
            driver.get(url)
            
            # Wait for the main container to be present
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ExpBox-root.mui-gp5f1p')))
            
            # Get page source and parse with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            main = soup.find(class_='ExpBox-root mui-gp5f1p')
            if not main:
                logger.error(f"No main container for {url}")
                return {'Source Link':url,'Company Name': '', 'Website': '', 'Domain': '', 'Company Description': '', 'Address': '', 'Phone Number': '', 'Email': '', 'Company Linkedin Page': '', 'Year Founded': '', 'Employees': '', 'Revenue': '', 'Number of locations': '', 'NAICS': '', 'SIC': ''}
            
            upper = main.find('div', class_='ExpBox-root mui-1i7seeh')
            if not upper:
                logger.error(f"No upper container for {url}")
                return {'Source Link':url,'Company Name': '', 'Website': '', 'Domain': '', 'Company Description': '', 'Address': '', 'Phone Number': '', 'Email': '', 'Company Linkedin Page': '', 'Year Founded': '', 'Employees': '', 'Revenue': '', 'Number of locations': '', 'NAICS': '', 'SIC': ''}
            
            heading = upper.find('h1', class_='ExpTypography-root ExpTypography-h1 mui-7s8p6g')
            company_name = heading.text.strip() if heading else ''
            
            intro = upper.find('p', class_='ExpTypography-root ExpTypography-body1 mui-18an9j9')
            description = intro.span.text.strip() if intro and intro.span else intro.text.strip() if intro else ''
            
            info = upper.find('div', attrs={'data-id': 'info-url'})
            domain = info.p.text.strip() if info and info.p else ''
            
            domain_p_list = upper.find_all('p', class_="ExpTypography-root ExpTypography-body1 ExpTypography-noWrap mui-1460r32")
            address = domain_p_list[1].text.strip() if len(domain_p_list) > 1 else ''
            
            tele = upper.find('div', attrs={'data-id': 'info-telephone'})
            number = tele.a.text.strip() if tele and tele.a else ''
            
            mail = upper.find('div', attrs={'data-id': 'info-email'})
            email = mail.a.text.strip() if mail and mail.a else ''
            
            linked = upper.find('div', attrs={'data-id': 'info-linkedin'})
            linkedin = linked.a.get('href') if linked and linked.a else ''
            
            down = main.find(class_="ExpBox-root mui-4h9p7m")
            if not down:
                logger.error(f"No down container for {url}")
                return {'Source Link':url,'Company Name': '', 'Website': '', 'Domain': '', 'Company Description': '', 'Address': '', 'Phone Number': '', 'Email': '', 'Company Linkedin Page': '', 'Year Founded': '', 'Employees': '', 'Revenue': '', 'Number of locations': '', 'NAICS': '', 'SIC': ''}
            
            details = down.find('div', class_="ExpBox-root mui-1134fyd")
            detail_list = details.find_all('p', class_="mui-7t1ht4")
            year = detail_list[0].text.strip() if len(detail_list) > 0 else ''
            revenue = detail_list[1].text.strip() if len(detail_list) > 1 else ''
            employees = detail_list[2].text.strip() if len(detail_list) > 2 else ''
            location = detail_list[3].text.strip() if len(detail_list) > 3 else ''
            
            NAICS = ''
            SIC = ''
            NS = details.find_all('p', class_="mui-cogau2")
            if len(NS) > 0:
                NAICS = NS[0].text.strip()
            if len(NS) > 1:
                SIC = NS[1].text.strip()
            
            logger.info(f"Scraped data for {company_name}")
            return {'Source Link':url,'Company Name': company_name, 'Website': 'https://www.' + domain, 'Domain': domain, 'Company Description': description, 'Address': address, 'Phone Number': number, 'Email': email, 'Company Linkedin Page': linkedin, 'Year Founded': year, 'Employees': employees, 'Revenue': revenue, 'Number of locations': location, 'NAICS': NAICS, 'SIC': SIC}
        except Exception as e:
            logger.error(f"Error processing {url} on attempt {attempt + 1}: {e}")
            time.sleep(2)  # Wait before retrying
        finally:
            if driver:
                driver.quit()
    
    logger.error(f"Failed to process {url} after {retries} attempts")
    return {'Source Link':url,'Company Name': '', 'Website': '', 'Domain': '', 'Company Description': '', 'Address': '', 'Phone Number': '', 'Email': '', 'Company Linkedin Page': '', 'Year Founded': '', 'Employees': '', 'Revenue': '', 'Number of locations': '', 'NAICS': '', 'SIC': ''}

def scrape(base_url):
    session = requests.Session() 
    all_data = []
    
    links = scrape_page(session, base_url)
    if not links:
        logger.error(f"No links found for {base_url}")
        return []

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(page, links))
        all_data.extend(results)
    
    return all_data    

for i in range(1,16):
    url = 'https://www.explorium.ai/manufacturing/search/b/page/'+str(i)+'/'   
    scraped_data = scrape(url)
    if scraped_data:
        df = pd.DataFrame(scraped_data)
        df.to_csv('scraped_links_B_'+str(i)+'.csv', index=False)
        logger.info(f'scraped_links_B_{i}.csv saved successfully')
    else:
        logger.info(f"No data scraped for {url}")