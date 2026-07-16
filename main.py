import requests
from bs4 import BeautifulSoup
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


def start(soup: BeautifulSoup) -> list[str]:
    cards = soup.find_all('a', class_='vw_crlnk')
    card_names = soup.find_all('a', class_='uni_lnk')

    uni_links = [card.get('href') for card in cards]
    uni_names = [name.get_text(strip=True) for name in card_names]
    return (uni_links, uni_names)

def get_course_links(soup: BeautifulSoup, url: str) -> list[str]:
    pass


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

        

main()