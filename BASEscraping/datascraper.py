import gspread
from gspread_dataframe import set_with_dataframe, get_as_dataframe
from oauth2client.service_account import ServiceAccountCredentials
import newspaper
from newspaper import ArticleException, Article
import pandas as pd
import nltk
from datetime import datetime, timedelta
import pytz
import os
import time
import requests

# Download some dependencies
nltk.download("punkt")

def download_article_with_retry(article):
    max_retries = 3
    retry_delay = 3  # seconds
    for retry_count in range(max_retries):
        try:
            article.download()
            article.parse()
            article.nlp()
            return True  # Success
        except ArticleException as e:
            print(f"Error downloading article from {article.url}: {str(e)}")
            time.sleep(retry_delay)
    return False  # All retries failed

def webscraping(urls, parsed_urls, search_keywords):
    articles_data = []
    current_time = datetime.now()
    search_keywords_set = [keyword.lower() for keyword in search_keywords]
    for website in urls:
        paper = newspaper.build(website, memoize_articles=False)
        for article in paper.articles: 
            if not article.url in parsed_urls:
                # Download the article with retries
                if download_article_with_retry(article):
                    if article.publish_date: # check if the article has a valid date format - avoid parsing videos
                        publish_date = article.publish_date.replace(tzinfo=None)
                        # Check if the article's publish date is within the past 24 hours
                        if (current_time - publish_date) < timedelta(days=5): 
                            article_keywords = article.keywords   
                            text_keywords = [keyword.lower() for keyword in article_keywords]
                            # Advanced NLP  only for relevant articles
                            if any(keyword in search_keywords_set for keyword in text_keywords):
                                # Extract the information you want from the article
                                title = article.title
                                url = article.url
                                summary = article.summary
                                print(f"Article title: {title} \n")
                                # Store the metadata in a dictionary
                                # Added the article and summary because we need them (summary for newsletter and article for wordclowds)
                                article_data = {
                                    "Title": title,
                                    "Publish Date": publish_date,
                                    "Summary": summary,
                                    "URL": url,
                                    "Keywords": article_keywords
                                }
                                # Append the dictionary to the list
                                articles_data.append(article_data)
    df = pd.DataFrame(articles_data) # Create a DataFrame from the list of dictionaries
    return df

def webscraping_and_save():
    # Define the scope and credentials file (JSON key file)
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    # Construct the path to the JSON key file using the GITHUB_WORKSPACE environment variable
    json_keyfile_path = os.path.join(os.environ['GITHUB_WORKSPACE'], 'hack4good-newsletter-5c61bf7e7811.json')
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_path, scope)    
    # google sheets authorization
    gc = gspread.authorize(credentials)
    # Open the Google Sheet and select the "URLs" worksheet
    url_sheet = gc.open("Prod_BASEconfig").worksheet("URLs")
    url_data = url_sheet.get_all_records()
    urls_df = pd.DataFrame(url_data)
    urls = urls_df['URL'].tolist()    
    # Open the Google Sheet and select the "Keywords" worksheet
    keyword_sheet = gc.open("Prod_BASEconfig").worksheet("Search Category")
    keyword_data = keyword_sheet.get_all_records()
    keyword_df = pd.DataFrame(keyword_data)
    keywords = keyword_df['Article Categories'].tolist()
    # Open the Google Sheet and select the visited URLs
    visited_websites = gc.open("Prod_BASEArticles").worksheet("WebScraping")
    visited_url_data = visited_websites.get_all_records()
    visited_url_df = pd.DataFrame(visited_url_data)
    visited_urls = visited_url_df['URL'].tolist()
    # Scrape new data
    df = webscraping(urls, visited_urls, keywords)
    # Open the Google Sheet by its title or URL
    spreadsheet = gc.open('Prod_BASEArticles')
    # Select a specific worksheet within the Google Sheet
    worksheet = spreadsheet.worksheet('WebScraping')  # Use 0 for the first worksheet    
    # Load existing data into a DataFrame
    existing_data = get_as_dataframe(worksheet, evaluate_formulas=True, dtype=str)
    existing_data.dropna(how="all", inplace=True)  # Drop empty rows   
    existing_data["Publish Date"] = pd.to_datetime(existing_data["Publish Date"], errors='coerce') 
     # Check if the DataFrame is non-empty before proceeding
    if not df.empty:
        # Convert the "Publish Date" column to datetime format
        df["Publish Date"] = pd.to_datetime(df["Publish Date"], errors='coerce')
        # Append new data to existing data
        combined_data = pd.concat([existing_data, df], ignore_index=True)
        # Filter out old entries (older than 14 day)
    else:
        print("The scraped data is empty. No data will be saved to the Google Sheet.")
        combined_data = existing_data
    current_time = datetime.now()  # Ensure that 'current_time' is timezone-aware if needed
    filtered_data = combined_data[combined_data["Publish Date"] >= current_time - timedelta(days=14)]    
    # Drop Duplicates
    filtered_data = filtered_data.drop_duplicates(subset='Title', keep='first')
    filtered_data = filtered_data.reset_index(drop=True)
    # Clear the worksheet before updating
    worksheet.clear()
    # Save the filtered data back to the worksheet
    set_with_dataframe(worksheet, filtered_data, include_index=False)

# Call the function to run the web scraping and data saving
webscraping_and_save()