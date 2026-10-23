import scraper
import excel_maker

def main():
    print("Welcome to the Top Unis Spreadsheet Generator!")
    print("Leave fields blank to use default values (Mechanical Engineering).")

    ranking_url = input("Enter the ranking URL: ").strip()
    course_keyword = input("Enter the course keyword to filter by (e.g., 'mechanical'): ").strip()

    # Use defaults if inputs are empty
    if not ranking_url:
        ranking_url = 'https://www.thecompleteuniversityguide.co.uk/league-tables/rankings/mechanical-engineering'
    if not course_keyword:
        course_keyword = 'mechanical'

    print(f"\nStarting the university scraper for '{course_keyword}' courses...")
    scraper.main(ranking_url, course_keyword)
    print("Scraping finished.")

    print("Generating Excel spreadsheet...")
    excel_maker.generate_excel()
    print("Spreadsheet generation finished.")

if __name__ == "__main__":
    main()
