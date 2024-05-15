import requests
from bs4 import BeautifulSoup

# URL of the webpage to scrape
url = "https://china.nba.cn/player/1628369"  # Replace with the actual URL

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table (assuming it's the first table in the page)
    table = soup.find('table')
    print(table)
    # Extract the headers
    headers = [th.text.strip() for th in table.find_all('th')]

    # Extract the rows
    rows = []
    for tr in table.find_all('tr'):
        cells = [td.text.strip() for td in tr.find_all('td')]
        if cells:
            rows.append(cells)

    # Print the extracted data
    print("Headers:", headers)
    print("Rows:")
    for row in rows:
        print(row)
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")


