import csv
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag


RANKING_URL = (
    "https://www.thecompleteuniversityguide.co.uk/"
    "league-tables/rankings/mechanical-engineering"
)

TIMEOUT_SECONDS = 15
OUTPUT_FILE = "university_requirements.csv"


def get_soup(
    session: requests.Session,
    url: str,
) -> BeautifulSoup | None:
    """Download and parse one webpage."""

    try:
        response = session.get(url, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()

    except requests.RequestException as error:
        print(f"Failed to download {url}: {error}")
        return None

    return BeautifulSoup(response.text, "html.parser")


def extract_universities(
    soup: BeautifulSoup,
    page_url: str,
) -> list[dict[str, str]]:
    """Extract university names and links from the ranking page."""

    universities: list[dict[str, str]] = []

    university_links = soup.find_all(
        "a",
        class_="vw_crlnk",
    )

    for link_element in university_links:
        if not isinstance(link_element, Tag):
            continue

        href = link_element.get("href")

        if not isinstance(href, str):
            continue

        university_url = urljoin(page_url, href)

        # Replace this depending on where the name appears.
        name = link_element.get_text(" ", strip=True)

        universities.append({
            "name": name,
            "url": university_url,
        })

    return universities


def extract_courses(
    soup: BeautifulSoup,
    university_url: str,
) -> list[dict[str, str]]:
    """Extract course names and links from one university page."""

    courses: list[dict[str, str]] = []

    # Replace this selector with the real course-link class.
    course_links = soup.find_all(
        "a",
        class_="course-link",
    )

    for link_element in course_links:
        if not isinstance(link_element, Tag):
            continue

        href = link_element.get("href")

        if not isinstance(href, str):
            continue

        course_name = link_element.get_text(" ", strip=True)
        course_url = urljoin(university_url, href)

        courses.append({
            "name": course_name,
            "url": course_url,
        })

    return courses


def extract_requirements(
    soup: BeautifulSoup,
) -> str | None:
    """Extract grade requirements from one course page."""

    # Best case: the requirement has a stable class.
    requirement_element = soup.find(
        class_="entry-requirements",
    )

    if isinstance(requirement_element, Tag):
        return requirement_element.get_text(
            " ",
            strip=True,
        )

    # Fallback: find an Entry Requirements heading.
    for heading in soup.find_all(
        ["h1", "h2", "h3", "h4"],
    ):
        if not isinstance(heading, Tag):
            continue

        heading_text = heading.get_text(
            " ",
            strip=True,
        ).lower()

        if "entry requirements" not in heading_text:
            continue

        next_element = heading.find_next(
            ["p", "div", "ul"],
        )

        if isinstance(next_element, Tag):
            return next_element.get_text(
                " ",
                strip=True,
            )

    return None


def save_results(
    results: list[dict[str, str]],
) -> None:
    """Save all course requirements to CSV."""

    fieldnames = [
        "university",
        "course",
        "requirements",
        "university_url",
        "course_url",
    ]

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(results)


def main() -> None:
    results: list[dict[str, str]] = []

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
            RANKING_URL,
        )

        if ranking_soup is None:
            return

        universities = extract_universities(
            ranking_soup,
            RANKING_URL,
        )

        print(f"Found {len(universities)} universities.")

        for university_number, university in enumerate(
            universities,
            start=1,
        ):
            university_name = university["name"]
            university_url = university["url"]

            print(
                f"\nUniversity "
                f"{university_number}/{len(universities)}: "
                f"{university_name}"
            )

            university_soup = get_soup(
                session,
                university_url,
            )

            if university_soup is None:
                continue

            courses = extract_courses(
                university_soup,
                university_url,
            )

            print(f"Found {len(courses)} courses.")

            for course_number, course in enumerate(
                courses,
                start=1,
            ):
                course_name = course["name"]
                course_url = course["url"]

                print(
                    f"  Course "
                    f"{course_number}/{len(courses)}: "
                    f"{course_name}"
                )

                course_soup = get_soup(
                    session,
                    course_url,
                )

                if course_soup is None:
                    continue

                requirements = extract_requirements(
                    course_soup,
                )

                if requirements is None:
                    requirements = "Not found"

                print(f"    Requirements: {requirements}")

                results.append({
                    "university": university_name,
                    "course": course_name,
                    "requirements": requirements,
                    "university_url": university_url,
                    "course_url": course_url,
                })

                # Save after every course so progress is not lost.
                save_results(results)

                time.sleep(1)

    print(
        f"\nFinished. Saved {len(results)} courses "
        f"to {OUTPUT_FILE}."
    )


if __name__ == "__main__":
    main()