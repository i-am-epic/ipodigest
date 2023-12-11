import PyPDF2
import re

# Open the PDF file in read-binary mode
pdf_file = open('DRHP.pdf', 'rb')

# Create a PDF reader object
pdf_reader = PyPDF2.PdfReader(pdf_file)

# Extract text from the PDF file
text = ''
for page in pdf_reader.pages:
    text += page.extract_text()


offer_price = None
if 'Offer Price: ' in text:
    offer_price = float(text.split('Offer Price: ')[1].split()[0])

# Extract the issue size
issue_size = None
if 'Issue Size: ' in text:
    issue_size = float(re.findall(r'(?<=Issue Size: )\d+(?:\.\d+)?', text)[0])

# Extract the company name
company_name = None
if 'COMPANY NAME' in text:
    company_name = re.findall(r'(?<=COMPANY NAME: ).*', text)[0]

print('Offer Price:', offer_price)
print('Issue Size:', issue_size)
print('Company Name:', company_name)

# Extract the offer price
offer_price = float(text.split('Offer Price: ')[1].split()[0])

# Extract the P/E ratio
pe_ratio = float(text.split('Price/Earnings Ratio ')[1].split()[0])

# Extract the number of shares being offered
num_shares = float(text.split('No. of Equity Shares offered')[1].split()[0])

# Calculate the market capitalization
market_cap = offer_price * num_shares

# Extract the revenue growth rate
revenue_growth = float(text.split('Revenue Growth')[1].split()[0])

# Extract the industry analysis
industry_analysis = text.split('Industry Overview')[1].split('Our Business')[0]

# Extract the use of proceeds
use_of_proceeds = text.split('Object of the Issue')[
    1].split('Our Strengths')[0]

# Extract the promoters' background
promoters_background = text.split('Promoters and Promoter Group')[
    1].split('Our Management')[0]


# Print the extracted data
print('Offer Price:', offer_price)
print('P/E Ratio:', pe_ratio)
print('Number of Shares:', num_shares)
print('Market Capitalization:', market_cap)
print('Revenue Growth Rate:', revenue_growth)
print('Industry Analysis:', industry_analysis)
print('Use of Proceeds:', use_of_proceeds)
print('Promoters Background:', promoters_background)


# Extract the financial statements
financials = {}
for section in re.findall(r'(CONSOLIDATED )?(AUDITOR)?(IND AS)?(IFRS)?(STANDALONE )?FINANCIAL (?:STATEMENT|SUMMARY).*?(?:Rs\.|`)', text, re.DOTALL):
    statement_type = re.findall(
        r'(CONSOLIDATED )?(AUDITOR)?(IND AS)?(IFRS)?(STANDALONE )?FINANCIAL', section, re.IGNORECASE)[0].strip().lower()
    statement_type = 'consolidated' if 'consolidated' in statement_type else 'standalone'
    statement_name = re.findall(r'(STATEMENT|SUMMARY)', section, re.IGNORECASE)[
        0].strip().lower()
    # Extract the financial statement data
    financials[f'{statement_type}_{statement_name}'] = re.findall(
        r'(?:^|\n)(.*?)(?:Rs\.|`)', section, re.DOTALL)[1:]

# Extract the business model and industry analysis
business_model = re.findall(
    r'(?<=Business\s+model\s+and\s+industry\s+overview).*?(?=Our\s+business)', text, re.DOTALL)[0]
industry_analysis = re.findall(
    r'(?<=Industry\s+overview).*?(?=Our\s+business)', text, re.DOTALL)[0]

# Extract the risk factors
risk_factors = re.findall(
    r'(?<=Risk\s+factors).*?(?=Our\s+business)', text, re.DOTALL)[0]

# Extract the promoter shareholding
promoter_shareholding = re.findall(
    r'(?<=Shareholding\s+of\s+promoters\s+and\s+promoter\s+group).*?(?=Our\s+management)', text, re.DOTALL)[0]

# Extract the board of directors
board_of_directors = re.findall(
    r'(?<=Board\s+of\s+directors).*?(?=Our\s+management)', text, re.DOTALL)[0]

# Extract the legal and regulatory compliance
compliance = re.findall(
    r'(?<=Legal\s+and\s+regulatory\s+compliance).*?(?=Our\s+business)', text, re.DOTALL)[0]

# Extract the offering structure
offering_structure = re.findall(
    r'(?<=Offering\s+structure).*?(?=Our\s+strengths)', text, re.DOTALL)[0]

# Close the PDF file
pdf_file.close()

# Print the extracted data
print('Financials:', financials)
print('Business Model:', business_model)
print('Industry Analysis:', industry_analysis)
print('Risk Factors:', risk_factors)
print('Promoter Shareholding:', promoter_shareholding)
print('Board of Directors:', board_of_directors)
print('Legal and Regulatory Compliance:', compliance)
print('Offering Structure:', offering_structure)
