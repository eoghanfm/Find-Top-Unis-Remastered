import requests
from bs4 import BeautifulSoup

response = requests.get("https://www.thecompleteuniversityguide.co.uk/courses/details/beng-mechanical-engineering-with-a-year-in-industry/58431474#entry_requirement")

soup = BeautifulSoup(response.text, "html.parser")

#a = soup.find_all("a", class_="pr_crinf")

#for link in a:
#    print(link.get('href'))
#print(len(a))

requirement = soup.find('p', class_='ucas_pt').get_text(strip=True)
print(requirement)
