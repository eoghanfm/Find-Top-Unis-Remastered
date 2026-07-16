import requests
from bs4 import BeautifulSoup

url = 'https://www.thecompleteuniversityguide.co.uk/league-tables/rankings/mechanical-engineering'

response = requests.get(url, timeout=10)
response.raise_for_status()  # Raise an error for bad responses

soup = BeautifulSoup(response.text, 'html.parser')

print(soup.prettify())  # Print the parsed HTML for inspection
