import scraper
import excel_maker

def main():
    print("Starting the university scraper...")
    scraper.main()
    print("Scraping finished.")

    print("Generating Excel spreadsheet...")
    excel_maker.generate_excel()
    print("Spreadsheet generation finished.")

if __name__ == "__main__":
    main()
