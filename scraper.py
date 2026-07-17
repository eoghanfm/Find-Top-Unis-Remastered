import requests
from bs4 import BeautifulSoup, soup
from urllib.parse import urljoin

initial_url = 'https://www.thecompleteuniversityguide.co.uk/league-tables/rankings/mechanical-engineering'

def get_soup(session: requests.Session, url: str) -> BeautifulSoup | None:
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()  # Raise an error for bad responses
    except requests.RequestException as e:
        print(f"Failed to download page {url}: {e}")
        return None
    
    return BeautifulSoup(response.text, 'html.parser')


def start(soup: BeautifulSoup) -> tuple[list[str], list[str]]:
    cards = soup.find_all('a', class_='vw_crlnk')
    card_names = soup.find_all('a', class_='uni_lnk')

    uni_links = []
    #uni_links = [card.get('href') for card in cards]
    for card in cards:
        href = card.get('href')
        if href:
            full_url = urljoin(initial_url, href)
            uni_links.append(full_url)
    
    uni_names = [name.get_text(strip=True) for name in card_names]
    return (uni_links, uni_names)

def get_course_links(session: requests.Session, soup: BeautifulSoup, url: str) -> list[str]:
    course_links = []
    
    while True:
        all_course_links = soup.find_all('a', class_='pr_crinf')
    
        for link in all_course_links:
            href = link.get('href')
            if href:
                full_url = urljoin(url, href)
                course_links.append(full_url)
        
        next_arrow = soup.select_one('nav.pg_nav.desk_pg a[aria-label="Next"]')
        if not next_arrow:
            break

        next_href = next_arrow.get("href")
    
        if not isinstance(next_href, str):
            break
        
        
        if next_href.strip().lower().startswith("javascript:"):
            break

        next_page_url = urljoin(url, next_href)

        next_soup = get_soup(session, next_page_url)

        if next_soup is None:
            break

        url = next_page_url
        soup = next_soup

    
    
    return course_links

def get_course_requirement(soup: BeautifulSoup) -> str | None:
    requirement = soup.find('p', class_='ucas_pt')
    if requirement:
        return requirement.get_text(strip=True)
    else:
        return None
    
def main():
    with requests.Session() as session:
        session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "Chrome/142.0 Safari/537.36"
            ),
            "Accept-Language": "en-GB,en;q=0.9",
        })

        ranking_soup = get_soup(
            session,
            initial_url,
        )

        uni_links, uni_names = start(ranking_soup)

        for uni_link in uni_links:
            uni_soup = get_soup(session, uni_link)
            course_links = get_course_links(uni_soup, uni_link)

            for course_link in course_links:
                course_soup = get_soup(session, course_link)
                requirement = get_course_requirement(course_soup)
                print(f"Course URL: {course_link}")
                print(f"Requirement: {requirement}\n")
            

main()