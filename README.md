# Top Unis Spreadsheet Generator

A Python tool that scrapes university rankings and course requirements from [The Complete University Guide](https://www.thecompleteuniversityguide.co.uk/), and generates a clean, filterable Excel spreadsheet of the results.

By default, it scrapes Mechanical Engineering courses, but it can be configured via terminal prompts to scrape data for any course keyword and ranking URL.

## Features

- **Automated Web Scraping:** Uses `BeautifulSoup` to navigate the Complete University Guide and extract ranking and entry requirement data.
- **Dynamic Course Filtering:** Prompts the user for a course keyword to filter out unrelated courses.
- **Progress Saving:** Automatically saves progress to `universities.json` so that if the scraper crashes or is stopped, it can resume where it left off.
- **Excel Spreadsheet Generation:** Uses `openpyxl` to generate a formatted Excel spreadsheet (`uni thing.xlsx`) complete with autofilters.
- **Hardcoded Filters:** Skips certain universities (like Imperial College London, Oxford, and Cambridge) during spreadsheet generation to filter out top-tier outliers.

## Prerequisites

- Python 3.10+
- The dependencies listed in `requirements.txt`.

## Installation

1. Clone or download this repository.
2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Usage

Run the main pipeline script:

```bash
python main.py
```

Upon running, the script will prompt you for:
1. **Ranking URL:** The URL of the league table you want to scrape (e.g., `https://www.thecompleteuniversityguide.co.uk/league-tables/rankings/computer-science`). Leave blank to use the default Mechanical Engineering URL.
2. **Course Keyword:** The keyword to filter courses by (e.g., `computer`). Leave blank to use the default `mechanical`.

The script will then scrape the universities, save the intermediate JSON data, and finally generate `uni thing.xlsx`.
