# Web Scraping Projects

This repository demonstrates various web scraping techniques using tools like Requests, BeautifulSoup, and Selenium.

---

## Scraping Basics

This section introduces fundamental scraping methods:

1. **Static Scraping** (e.g., Wikipedia pages):
   - Tools: Requests, BeautifulSoup.
2. **Dynamic Scraping** (e.g., example domain):
   - Tool: Selenium.
   - Workflow: Start WebDriver → Navigate Pages → Locate Elements → Handle Dynamic Content.

---

## Glassdoor Scraper

A project to extract job data from Glassdoor using Selenium.

- **WebDriver Setup**: Includes user-agent rotation and anti-detection measures.
- **Dynamic Content Handling**: Waits for page elements to fully load.
- **Output**: Saves data into `jobs_data_output.csv`.

---

## Upwork Scraper

A project to scrape Upwork profiles and job data, organized into modular scripts:

- `setup_environment.py`: Prepares the scraping environment.
- `explore_data.py`: Explores and analyzes scraped data.
- `scrape_detail.py`: Scrapes detailed profile information.
- `scrape_profile.py`: Extracts general profile data.
- `scrape_ranking.py`: Collects ranking and performance metrics.
- `connect_database.py`: Handles database connections.


