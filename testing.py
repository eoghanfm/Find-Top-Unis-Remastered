import requests
from bs4 import BeautifulSoup

response = requests.get("https://www.thecompleteuniversityguide.co.uk/league-tables/rankings/mechanical-engineering")

soup = BeautifulSoup(response.text, "html.parser")

a = soup.find_all('span', class_='uninum')


for link in a:
    print(link.get_text(strip=True))
print(len(a))


#requirement = soup.find('span', class_='ucanxtarw')
#print(requirement)
