import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from time import sleep
import random

from json_handler import save_progress, load_progress

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
        if href and not href.strip().lower().startswith("javascript:"):  # Ignore JavaScript links
            full_url = urljoin(initial_url, href)
            full_url = full_url.replace("/clearing", "")  # Remove "/clearing" from the URL
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
    EXTRA_DELAY = 0 # add more delay if website crashes
    failed_requests = 0
    
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

        ## EXAMPLE STRUCTURE ##
        #unis = {
        #   "Imperial College London": : [
        #       {"name": "Mechanical Engineering", "requirement": "AAB"},
        #       {"name": "Aerospace Engineering", "requirement": "AAA"},
        #    ],
        #   "Cambdridge University": [...
        # },
        unis = load_progress()  # Load progress if exists

        repeat = 50  # ask user

        it = -1
        for uni_link in uni_links:
            it += 1
            if it >= len(uni_links)-1:
                break

            if uni_names[it] in unis:
                print(f"Skipping completed university: {uni_names[it]}")
                continue  # Skip already processed universities


            print(f"Processing university {it + 1}/{len(uni_links)}: {uni_names[it]}")
 
            uni_soup = get_soup(session, uni_link)

            course_info = get_courses(session, uni_soup, uni_link)

            individual_uni = []

            for course in course_info:
                # filter courses
                if "mechanical" not in course["name"].lower():
                    continue

                print(f"Processing course: {course['name']}")

                course_link = course["url"]
                
                for attempt in range(3):  # Retry up to 3 times
                    course_soup = get_soup(session, course_link)
                    if course_soup is not None:
                        break
                    
                    print(f"Retrying ({attempt + 1}/3) for course: {course['name']}")
                    sleep(10)
                    EXTRA_DELAY += 0.7
                    failed_requests += 1
                    if failed_requests >= 3:
                        print("Too many failed attempts. Exiting program.")
                        exit(1)
                else:
                    continue  # Skip this course if all attempts fail

                
                requirement = get_course_requirement(course_soup)

                individual_uni.append({
                    "name": course["name"],
                    "requirement": requirement if requirement else "N/A"
                    }
                )

                sleep(random.uniform(1, 1.4) + EXTRA_DELAY)
            
            print()
            print()
            
            unis[uni_names[it]] = individual_uni
            save_progress(unis)  # Save progress after each university

    return unis

if __name__ == "__main__":
    main()