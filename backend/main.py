import time
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import requests
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware
import httpx
from typing import Optional
from datetime import datetime
import re
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# app = FastAPI()
# # Allow specific origins
# origins = [
#     "http://localhost:3000",  # Your frontend origin
# ]


# # Configure CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allows all origins. Replace "*" with specific domains for more control
#     allow_credentials=True,
#     allow_methods=["*"],  # Allows all HTTP methods
#     allow_headers=["*"],  # Allows all headers
# )


# @app.get("/ipos")
# def read_ipos():
#     return {"ipos": "List of IPOs"}

# # Replace with your actual SEBI URL
# SEBI_URL = "https://www.sebi.gov.in/sebiweb/home/HomeAction.do?doListing=yes&sid=3&ssid=15&smid=10"

# HEADERS = {
#     "Host": "www.sebi.gov.in",
#     "Cache-Control": "max-age=0",
#     "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
#     "Sec-Ch-Ua-Mobile": "?0",
#     "Sec-Ch-Ua-Platform": "macOS",
#     "Accept-Language": "en-GB",
#     "Upgrade-Insecure-Requests": "1",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#     "Sec-Fetch-Site": "none",
#     "Sec-Fetch-Mode": "navigate",
#     "Sec-Fetch-User": "?1",
#     "Sec-Fetch-Dest": "document",
#     "Accept-Encoding": "gzip, deflate, br",
#     "Priority": "u=0, i",
#     "Connection": "keep-alive",
# }


# COOKIES = {
#     "JSESSIONID": "965BF997B85D296C667C74CC5B2D1AE8",
#     "_ga": "GA1.3.584588982.1728339869",
#     "_gid": "GA1.3.334062939.1728339869",
#     "_ga_9HZ5J5Q3K5": "GS1.3.1728339869.1.1.1728339981.60.0.0",
#     "_gat": "1",
# }


# @app.get("/companies")
# def get_companies():
#     # Send the request to SEBI page
#     response = requests.get(SEBI_URL, headers=HEADERS, cookies=COOKIES)

#     if response.status_code != 200:
#         return {"error": "Failed to retrieve data"}

#     # Parse the HTML content
#     soup = BeautifulSoup(response.content, "html.parser")

#     # List to store company data
#     companies = []

#     # Find all table rows that have 'tr' tag with class 'odd' or 'even'
#     for row in soup.find_all("tr", class_=["odd", "even"]):  # Handles both 'odd' and 'even' rows
#         date = row.find("td").text.strip()  # Get the date from the first 'td' tag
#         company_link_tag = row.find("a")  # Find the <a> tag with company info
        
#         if company_link_tag:
#             company_name = company_link_tag.text.strip()  # Get company name
#             company_link = company_link_tag['href']  # Get company link
            
#             # Append the extracted data to the companies list
#             companies.append({
#                 "date": date,
#                 "company_name": company_name,
#                 "link": company_link
#             })

#     return {"companies": companies}

# @app.get("/scrape-ipo")
# async def scrape_ipo():
#     url = 'https://www.investorgain.com/report/live-ipo-gmp/331/'
#     response = requests.get(url)
#     html_content = response.content

#     soup = BeautifulSoup(html_content, 'html.parser')

#     ipo_data = []
#     table = soup.find('table', id='mainTable')
#     if table:
#         rows = table.find('tbody').find_all('tr')
#         for row in rows:
#             columns = row.find_all('td')
#             if len(columns) == 12:
#                 ipo_info = {
#                     'company_name': columns[0].get_text(strip=True),
#                     'price': columns[1].get_text(strip=True),
#                     'gmp': columns[2].get_text(strip=True),
#                     'est_listing': columns[3].get_text(strip=True),
#                     'fire_rating': columns[4].find('img')['alt'] if columns[4].find('img') else '',
#                     'ipo_size': columns[5].get_text(strip=True),
#                     'lot': columns[6].get_text(strip=True),
#                     'open_date': columns[7].get_text(strip=True),
#                     'close_date': columns[8].get_text(strip=True),
#                     'boa_date': columns[9].get_text(strip=True),
#                     'listing_date': columns[10].get_text(strip=True),
#                     'gmp_updated': columns[11].get_text(strip=True)
#                 }
#                 ipo_data.append(ipo_info)

#     return JSONResponse(content=ipo_data)

# @app.get("/scrape-ipo-tables")
# async def scrape_ipo_tables():
#     # Headers to mimic browser requests
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#     }
#     # URL to scrape
#     url = "https://www.nseindia.com/market-data/all-upcoming-issues-ipo"
    
#     # Make a request to the webpage
#     response = requests.get(url, headers=headers)
    
#     # Check if the request was successful
#     if response.status_code != 200:
#         return {"error": "Failed to fetch the webpage"}

#     # Parse the HTML content using BeautifulSoup
#     soup = BeautifulSoup(response.content, 'html.parser')
    
#     # Find the container with class "tab-content py-3"
#     tab_content = soup.find('div', {'class': 'tab-content py-3'})
    
#     if not tab_content:
#         return {"error": "The tab-content container was not found on the webpage"}
    
#     # A dictionary to hold table data for each tab
#     all_table_data = {}

#     # Define the IDs of each tab we want to scrape
#     tab_ids = ['ipo-current', 'ipo-past', 'ipo-upcoming']

#     # Iterate over each tab to find the relevant tables
#     for tab_id in tab_ids:
#         tab = tab_content.find('div', {'id': tab_id})
        
#         # Find the thead and tbody within this tab
#         if tab:
#             thead = tab.find('thead')
#             tbody = tab.find('tbody')
#             print(thead,tbody)
            
#             # If thead and tbody are found, process them
#             if thead and tbody:
#                 # Extract the headers
#                 headers = []
#                 for header_row in thead.find_all('tr'):
#                     for header in header_row.find_all('th'):
#                         headers.append(header.get_text(strip=True))
                
#                 # Extract rows from the tbody
#                 table_data = []
#                 for row in tbody.find_all('tr'):
#                     columns = row.find_all('td')
#                     # Ensure we only process rows with the same number of columns as headers
#                     if len(columns) == len(headers):
#                         row_data = {headers[i]: col.get_text(strip=True) for i, col in enumerate(columns)}
#                         table_data.append(row_data)
                
#                 # Add the table data to the dictionary with the tab ID as the key
#                 all_table_data[tab_id] = table_data
#             else:
#                 # If no thead or tbody is found, return an empty list for that tab
#                 all_table_data[tab_id] = []
#         else:
#             # If the tab is not found, add an error message
#             all_table_data[tab_id] = {"error": f"Tab with id {tab_id} not found"}

#     # Return the scraped data as JSON
#     return {"tables": all_table_data}

app = FastAPI(title="IPO Scraper API")
origins = [
    "http://localhost:3001",  # Your frontend origin
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


BASE_URL = "https://www.chittorgarh.com/report/ipo-in-india-list-main-board-sme/82/"

def setup_driver():
    """Setup Chrome driver with headless options"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Add additional arguments to make it more stable
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-infobars")
    
    return webdriver.Chrome(options=chrome_options)

def fetch_page_content():
    """
    Fetch page content using Selenium with proper wait conditions
    """
    driver = setup_driver()
    try:
        # Navigate to the page
        driver.get(BASE_URL)
        
        # Wait for the table to be present and visible
        wait = WebDriverWait(driver, 10)
        table = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "table"))
        )
        
        # Additional wait to ensure dynamic content is loaded
        time.sleep(2)
        
        # Get the page content
        content = driver.page_source
        return content
    finally:
        driver.quit()

def parse_price_band(price_band_text: str) -> dict:
    prices = re.findall(r'\d+\.?\d*', price_band_text)
    if len(prices) >= 2:
        return {
            "min": float(prices[0]),
            "max": float(prices[1])
        }
    return {"min": 0, "max": 0}

def parse_date(date_str: str) -> str:
    try:
        date_obj = datetime.strptime(date_str.strip(), "%b %d, %Y")
        return date_obj.strftime("%Y-%m-%d")
    except:
        return date_str

def parse_issue_size(size_text: str) -> float:
    try:
        clean_size = size_text.replace(',', '')
        return float(clean_size) * 10000000  # Convert Cr to absolute value
    except:
        return 0

def get_ipo_status(dates: dict) -> str:
    today = datetime.now()
    try:
        opens = datetime.strptime(dates["opens"], "%Y-%m-%d")
        closes = datetime.strptime(dates["closes"], "%Y-%m-%d")
        
        if today < opens:
            return "upcoming"
        elif opens <= today <= closes:
            return "current"
        else:
            return "past"
    except:
        return "unknown"

def scrape_ipos():
    """
    Scrape IPO data from the webpage
    """
    try:
        content = fetch_page_content()
        soup = BeautifulSoup(content, 'html.parser')
        ipo_list = []
        
        # Find the main IPO table
        tables = soup.find_all('table', {'class': 'table'})
        
        for table in tables:
            # Look for rows with specific classes
            rows = table.find_all('tr', {'class': ['color-green', 'color-lightyellow',"table table-bordered table-striped table-hover w-auto."]})
            
            for row in rows:
                try:
                    cols = row.find_all('td')
                    if len(cols) >= 8:
                        link = cols[0].find('a')
                        if not link:
                            continue
                            
                        subscription_dates = {
                            "opens": parse_date(cols[1].text),
                            "closes": parse_date(cols[2].text)
                        }
                        
                        ipo_data = {
                            "ipo_id": link['href'].split('/')[-2],
                            "company_name": link.text.strip(),
                            "symbol": "",  # Would need additional scraping
                            "status": get_ipo_status(subscription_dates),
                            "price_band": parse_price_band(cols[4].text),
                            "issue_size": parse_issue_size(cols[5].text),
                            "lot_size": int(cols[6].text.strip()),
                            "subscription_dates": subscription_dates,
                            "listing_date": parse_date(cols[3].text),
                            "category_wise_shares": {
                                "QIB": 50,
                                "NII": 25,
                                "retail": 25
                            },
                            "listing_at": cols[7].text.strip()
                        }
                        
                        ipo_list.append(ipo_data)
                except Exception as e:
                    print(f"Error processing row: {str(e)}")
                    continue
                    
        return ipo_list
    except Exception as e:
        print(f"Error scraping data: {str(e)}")
        return []

@app.get("/api/v1/ipo/list")
def get_ipo_list(
    status: Optional[str] = None,
    page: int = 1,
    limit: int = 10
):
    try:
        all_ipos = scrape_ipos()
        
        # Filter by status if specified
        if status:
            all_ipos = [ipo for ipo in all_ipos if ipo["status"] == status]
        
        # Calculate pagination
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paginated_ipos = all_ipos[start_idx:end_idx]
        
        return {
            "status": "success",
            "data": {
                "ipos": paginated_ipos,
                "total_count": len(all_ipos),
                "current_page": page
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Debug endpoint
@app.get("/api/v1/ipo/debug")
def debug_scrape():
    try:
        data = scrape_ipos()
        return {"status": "success", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))