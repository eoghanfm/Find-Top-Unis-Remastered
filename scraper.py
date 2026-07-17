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


def start(soup: BeautifulSoup) -> tuple[list[str], list[str]]:
    cards = soup.find_all('a', class_='vw_crlnk')
    card_names = soup.find_all('a', class_='uni_lnk')
    #ranking_numbers = soup.find_all('span', class_='uninum')

    uni_links = []
    for card in cards:
        href = card.get('href')
        if href:
            full_url = urljoin(initial_url, href)
            uni_links.append(full_url)
    
    uni_names = [name.get_text(strip=True) for name in card_names]
    return (uni_links, uni_names)

def get_courses(
    session: requests.Session,
    soup: BeautifulSoup,
    url: str,
) -> list[dict[str, str]]:
    courses: list[dict[str, str]] = []

    while True:
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

            if name_element is None or link_element is None:
                continue

            href = link_element.get("href")

            if not isinstance(href, str):
                continue

            course_name = name_element.get_text(
                " ",
                strip=True,
            )

            course_url = urljoin(url, href)

            courses.append({
                "name": course_name,
                "url": course_url,
            })

        next_arrow = soup.select_one(
            'nav.pg_nav.desk_pg a[aria-label="Next"]'
        )

        if next_arrow is None:
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

    return courses

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

        # get initial table of unis info
        uni_links, uni_names = start(ranking_soup)

        unis = []

        #for uni in uni_names:
        #    unis.append({
        #        "uniName": uni,
        #    })

        repeat = 3  # ask user

        it = 0
        for uni_link in uni_links:
            uni_soup = get_soup(session, uni_link)
            course_info = get_courses(session, uni_soup, uni_link)
            #print(course_info)

            for course in course_info:
                course_link = course["url"]
                course_soup = get_soup(session, course_link)
                requirement = get_course_requirement(course_soup)

                unis.append({
                    uni_names[it]: {
                        "courseName": course["name"],
                        "requirement": requirement,
                    }
                })
                print(f"Course URL: {course_link}")
                print(f"Requirement: {requirement}\n")
            
            it += 1
            if repeat >= it:
                break
            


main()