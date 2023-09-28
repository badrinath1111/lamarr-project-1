import requests
from bs4 import BeautifulSoup
import json

base_url = "https://www.scrapethissite.com/pages/forms/"

num_pages = 5

data = []

for page_num in range(1, num_pages + 1):
    page_url = f"{base_url}?page_num={page_num}"
    
    response = requests.get(page_url)
        
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', class_='table')
        
        if table:
            rows = table.find_all('tr')
            
            for row in rows[1:]:
                columns = row.find_all('td')
                row_data = {
                    'Team Name': columns[0].text.strip(),
                    'Year': columns[1].text.strip(),
                    'Wins': columns[2].text.strip(),
                    'Losses': columns[3].text.strip(),
                    'OT Losses': columns[4].text.strip(),
                    'Win %': columns[5].text.strip(),
                    'Goals For (GF)': columns[6].text.strip(),
                    'Goals Against (GA)': columns[7].text.strip(),
                    '+ / -': columns[8].text.strip(),
                }
                data.append(row_data)
        else:
            print(f"Table not found on page {page_num}.")
    else:
        print(f"Failed to retrieve page {page_num}. Status code: {response.status_code}")

with open('scraped_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print(f"Scraped data from {num_pages} pages and saved to scraped_data.json.")
