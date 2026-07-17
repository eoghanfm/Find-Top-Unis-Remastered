import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


url = requests.get("https://www.thecompleteuniversityguide.co.uk/courses/university-search/undergraduate/mechanical-engineering/imperial-college-london")

soup = BeautifulSoup(url.text, "html.parser")

"""
a = soup.find_all('span', class_='uninum')


for link in a:
    print(link.get_text(strip=True))
print(len(a))


#requirement = soup.find('span', class_='ucanxtarw')
#print(requirement)
"""

course_cards = soup.find_all(
            "div",
            class_="sr_cont",
        )

for card in course_cards:
    name_element = card.find("h3")
    link_element = card.find(
        "a",
        class_="pr_crinf",
    )

    print(name_element.get_text(strip=True) if name_element else "No name found")
    print(link_element.get("href") if link_element else "No link found")
    