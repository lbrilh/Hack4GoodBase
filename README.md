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
* Luca Brilhaus
* Leander Waddel
* Xueqing Wang

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
- `file.json`: A JSON key file for Google Sheets authentication.

## Getting Started

To get started with this project, follow these steps:

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/BASEProject.git
   cd BASEProject

We provide the user with a key word analytics tool and weekly newsletter containing summaries of current articles from multiple online sources. In particular, we created a pipeline including web scraping and aggregating information (using LLMs) relevant to energy servitization.

## Workflow Automation

This repository includes GitHub Actions workflows located in the `.github/workflows` folder. These workflows are designed to automate the execution of the web scraping and newsletter generation scripts based on specific triggers or schedules.

To set up and customize these workflows for your needs, refer to the workflow YAML files in the `.github/workflows` directory.

## Dependencies

The project relies on various Python packages for web scraping, data processing, and newsletter generation. Please refer to the `requirements.txt` and `install_packages.txt` files in the respective folders for a list of required dependencies.

## License

This project is licensed under the [License Name] License - see the [LICENSE](LICENSE) file for details.
