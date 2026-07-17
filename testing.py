import requests
from bs4 import BeautifulSoup

response = requests.get("https://www.thecompleteuniversityguide.co.uk/courses/university-search/postgraduate/all/university-of-cambridge?pg=23")

soup = BeautifulSoup(response.text, "html.parser")

a = next_arrow = soup.select_one(
    'nav.pg_nav.desk_pg a[aria-label="Next"]'
)

#for link in a:
#    print(link.get('href'))
print(len(a))
print(next_arrow.get('href'))

#requirement = soup.find('span', class_='ucanxtarw')
#print(requirement)
