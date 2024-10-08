from fastapi import FastAPI
from fastapi.responses import JSONResponse
import requests
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
# Allow specific origins
origins = [
    "http://localhost:3000",  # Your frontend origin
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ipos")
def read_ipos():
    return {"ipos": "List of IPOs"}

# Replace with your actual SEBI URL
SEBI_URL = "https://www.sebi.gov.in/sebiweb/home/HomeAction.do?doListing=yes&sid=3&ssid=15&smid=10"

HEADERS = {
    "Host": "www.sebi.gov.in",
    "Cache-Control": "max-age=0",
    "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "macOS",
    "Accept-Language": "en-GB",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Accept-Encoding": "gzip, deflate, br",
    "Priority": "u=0, i",
    "Connection": "keep-alive",
}

COOKIES = {
    "JSESSIONID": "965BF997B85D296C667C74CC5B2D1AE8",
    "_ga": "GA1.3.584588982.1728339869",
    "_gid": "GA1.3.334062939.1728339869",
    "_ga_9HZ5J5Q3K5": "GS1.3.1728339869.1.1.1728339981.60.0.0",
    "_gat": "1",
}


@app.get("/companies")
def get_companies():
    # Send the request to SEBI page
    response = requests.get(SEBI_URL, headers=HEADERS, cookies=COOKIES)

    if response.status_code != 200:
        return {"error": "Failed to retrieve data"}

    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # List to store company data
    companies = []

    # Find all table rows that have 'tr' tag with class 'odd' or 'even'
    for row in soup.find_all("tr", class_=["odd", "even"]):  # Handles both 'odd' and 'even' rows
        date = row.find("td").text.strip()  # Get the date from the first 'td' tag
        company_link_tag = row.find("a")  # Find the <a> tag with company info
        
        if company_link_tag:
            company_name = company_link_tag.text.strip()  # Get company name
            company_link = company_link_tag['href']  # Get company link
            
            # Append the extracted data to the companies list
            companies.append({
                "date": date,
                "company_name": company_name,
                "link": company_link
            })

    return {"companies": companies}

@app.get("/scrape-ipo")
async def scrape_ipo():
    url = 'https://www.investorgain.com/report/live-ipo-gmp/331/'
    response = requests.get(url)
    html_content = response.content

    soup = BeautifulSoup(html_content, 'html.parser')

    ipo_data = []
    table = soup.find('table', id='mainTable')
    if table:
        rows = table.find('tbody').find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            if len(columns) == 12:
                ipo_info = {
                    'company_name': columns[0].get_text(strip=True),
                    'price': columns[1].get_text(strip=True),
                    'gmp': columns[2].get_text(strip=True),
                    'est_listing': columns[3].get_text(strip=True),
                    'fire_rating': columns[4].find('img')['alt'] if columns[4].find('img') else '',
                    'ipo_size': columns[5].get_text(strip=True),
                    'lot': columns[6].get_text(strip=True),
                    'open_date': columns[7].get_text(strip=True),
                    'close_date': columns[8].get_text(strip=True),
                    'boa_date': columns[9].get_text(strip=True),
                    'listing_date': columns[10].get_text(strip=True),
                    'gmp_updated': columns[11].get_text(strip=True)
                }
                ipo_data.append(ipo_info)

    return JSONResponse(content=ipo_data)