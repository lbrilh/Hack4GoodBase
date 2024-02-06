# BASE Project Repository

This repository contains the code and resources for the BASE project (part of Hack4Good organized by ETH Zurich Analytics Club), which includes web scraping (`BASEScraping`) and newsletter generation (`BASENewsletter`) components.

## Table of Contents

- [Team Members](#team-members)
- [Project Overview](#project-overview)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Workflow Automation](#workflow-automation)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Team Members
* Luca Brilhaus (https://ch.linkedin.com/in/lucabrilhaus)
* Leander Waddell (https://ch.linkedin.com/in/leander-waddell-9b3163263)
* Xueqing Wang (https://ch.linkedin.com/in/wangxueqing)

## Project Overview

The BASE project focuses on web scraping and newsletter generation. It includes two main components:

- **BASEScraping:** This component (`BASEScraping`) is responsible for web scraping articles from specified websites. It uses the `newspaper` library to extract article information, including titles, publish dates, summaries, URLs, and keywords. The scraped data is then processed and updated in a Google Sheet for further analysis and archiving.

- **BASENewsletter:** The `BASENewsletter` component is designed to generate a weekly newsletter based on the scraped articles. It leverages natural language processing (NLP) techniques to filter and sort articles, translate them if necessary, and create an HTML email containing selected articles for distribution.

## Repository Structure

The repository has the following structure:

- `.github/workflows`: Contains GitHub Actions workflows for automating the execution of the web scraping and newsletter generation scripts.
- `BASEScraping`: Folder containing scripts and resources related to web scraping.
  - `datascraper.py`: Python script for web scraping and updating a Google Sheet.
  - `google_sheet_updates.py`: Python script for archiving and managing data in a Google Sheet.
  - `requirements.txt`: List of required Python packages.
- `BASENewsletter`: Folder containing scripts and resources for newsletter generation.
  - `WeeklyNewsletter.py`: Python script for generating a weekly newsletter using scraped articles.
  - `install_packages.txt`: List of required Python packages for the newsletter generation script.
- `.gitignore`: Configuration file to specify which files or directories should be ignored by Git.
- `LICENSE`: The license file for this project.
- `README.md`: This README file.
- `hack4good-newsletter-5c61bf7e7811.json`: A JSON key file for Google Sheets authentication.

## Getting Started

To get started with this project, follow these steps:

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/BASEProject.git
   cd BASEProject
   
2. Install the required Python packages for web scraping and newsletter generation. Refer to the `requirements.txt` and `install_packages.txt` files in the respective folders (BASEScraping and BASENewsletter) for package details.
  
3. Provide the necessary JSON key file `hack4good-newsletter-5c61bf7e7811.json` for Google Sheets authentication as specified in the scripts (Configure Google SHeets Authentication.

## Google Sheets Integration

For information regarding the use of Google Sheets to manage keywords, categories, URL storage, newsletter recipients, and how to use it as an archive, please contact one of the team members. 

Google Sheets is a crucial component of our project for managing various aspects of data and communication. For detailed guidance and assistance with setting up and using Google Sheets within the project, please reach out to one of our team members. They will provide you with the necessary instructions and access to these Google Sheets documents.


## Usage

### Web Scraping (BASEScraping)

1. Ensure that you have set up the Google Sheet where scraped data will be stored. Update the Google Sheet's name and worksheet names in the `datascraper.py` script.
2. Execute the web scraping script by running the `datascraper.py` script:

   ```bash
   python BASEScraping/datascraper.py

3. The script will scrape articles from specified websites, process the data, and update the Google Sheet with the latest information.

### Newsletter Generation (BASENewsletter)

1. Configure the newsletter generation script by updating the necessary parameters, such as search keywords and article categories, in the `WeeklyNewsletter.py` script.
2. Execute the newsletter generation script:

   ```bash
   python BASENewsletter/WeeklyNewsletter.py

3. The script will generate a weekly newsletter based on the scraped articles and send it to the specified recipients.

## Workflow Automation

This repository includes GitHub Actions workflows located in the `.github/workflows` folder. These workflows are designed to automate the execution of the web scraping and newsletter generation scripts based on specific triggers or schedules.

To set up and customize these workflows for your needs, refer to the workflow YAML files in the `.github/workflows` directory.

## Dependencies

The project relies on various Python packages for web scraping, data processing, and newsletter generation. Please refer to the `requirements.txt` and `install_packages.txt` files in the respective folders for a list of required dependencies.

## License

This project is licensed under the [License Name] License - see the [LICENSE](LICENSE) file for details.
