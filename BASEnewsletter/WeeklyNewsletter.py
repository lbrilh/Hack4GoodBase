# Python Built-in Package

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from email.mime.image import MIMEImage

from email.mime.base import MIMEBase
from email import encoders

import os
# os.chdir('C:\git-sdk-64\hack4goodbase')
from datetime import date

import pandas as pd

# from googletrans import Translator

# To install

import pygsheets
from sentence_transformers import SentenceTransformer, util

# google sheets authorization
gc = pygsheets.authorize(service_file='hack4good-newsletter-5c61bf7e7811.json')
# translator = Translator()

def read_gsheet(workbookname, worksheetname, ReadAsDF):
    sh = gc.open(workbookname)
    wks = sh.worksheet(property='title', value=worksheetname)
    if ReadAsDF:
        return wks.get_as_df()
    else:
        return wks.get_all_records()
    
def retrieve_scrapping_result_gsheet(sheet_name):
    
    articles = read_gsheet('Prod_BASEArticles', sheet_name, ReadAsDF=True)
    if sheet_name == 'WebScraping':
        articles = articles[['Title','Publish Date','Summary','URL','Keywords']]
    
    articles['Publish Date'] = pd.to_datetime(articles['Publish Date']).dt.date
    
    return articles

def translate_to_english(text):
    if translator.detect(text).lang == 'en':
        return None
    else:
        return translator.translate(text, src='auto', dest='en').text

def text_embedding(df, text_col_name, model):
    text_to_process = df[text_col_name]
    text_embeddings = model.encode(text_to_process)
    
    return text_embeddings.tolist()    

def archive_bulk_insert(latest_articles):
    sh = gc.open('Prod_BASEArticles')
    wks_archive = sh.worksheet(property='title', value='Archive')
    archives = wks_archive.get_as_df()
    
    latest_articles['label'] = 'new'
    archives['label'] = 'archive'
    
    all_articles = pd.concat([archives, latest_articles[archives.columns]])
    
    all_articles = all_articles.drop_duplicates(subset='Title', keep='first')
    
    all_articles = all_articles[all_articles['label']=='new'].drop('label', axis=1)
    all_articles['Publish Date'] = pd.to_datetime(all_articles['Publish Date'])
    all_articles['Publish Date'] = all_articles['Publish Date'].dt.strftime('%Y-%m-%d')
    
    wks_archive = sh.worksheet(property='title', value='Archive')
    
    if not all_articles.empty:
        wks_archive.append_table(all_articles.values.tolist(), overwrite=False)

    return

def filter_sort_articles():
    
    all_articles = retrieve_scrapping_result_gsheet(sheet_name='WebScraping')
    archived = retrieve_scrapping_result_gsheet(sheet_name='Archive')
    
    # Filter Articles - Part 1
    con1 = all_articles['URL'].isin(archived['URL'].tolist())==False
    con2 = all_articles['Title'].isin(archived['URL'].tolist())==False
    all_articles = all_articles[(con1)&(con2)]
    
    # drop duplicates
    all_articles = all_articles.drop_duplicates(subset='Title')
    
    # filter articles - Part 2:
    latest_article = all_articles[pd.to_timedelta(date.today() - all_articles['Publish Date'], unit='d')<=pd.to_timedelta(nb_days, unit='d')*2].copy()
    latest_article = latest_article.reset_index(drop=True)
    
#    # For articles in other languages: translate to EN
#    latest_article['Summary_EN'] = latest_article['Summary'].apply(lambda x: translate_to_english(x))
    latest_article['Summary_EN'] = None

    # Sort (based on translated summary)
    latest_article['Summary_ForSorting'] = latest_article['Summary_EN'].fillna(latest_article['Summary'])
    ## Generate Embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')

    latest_article['SUMMARY_EMBEDDING'] = text_embedding(latest_article, 'Summary_ForSorting', model)
    provided_search_keywords_embeddings = model.encode(provided_search_keywords)
    article_category_embeddings = model.encode(article_category)
    
    ## Calculate Similarities
    latest_article['MAX_SCORE_CATEGORY'] = 0
    latest_article['MAX_SCORE'] = 0
    latest_article['AVG_SCORE'] = 0
    latest_article['Most Relevant Keyword'] = ''
    latest_article['Prioritize'] = 0
    latest_article['Contains Keyword'] = ''
    
    for index, row in latest_article.iterrows():
        # Prioritize the article if any of the search keyword is found
        summary = row['Summary_ForSorting'].lower()
        contain_keyword_ind = [int((skw.lower() in summary) or (" ".join(skw.split("-")) in summary)) for skw in provided_search_keywords]
        contain_keywords = [provided_search_keywords[i] for i in range(len(provided_search_keywords)) if contain_keyword_ind[i]==1]
        contain_keywords = "; ".join(contain_keywords)
        prioritize_ind = max(contain_keyword_ind)
        
        summary_embedding = row['SUMMARY_EMBEDDING']
        
        # check similarities with respect to specific search keywords
        similarities = []
        for kw in provided_search_keywords_embeddings:
            similarities.append(util.cos_sim(kw, summary_embedding).item())
        similarity_max = max(similarities) 
        similarity_avg = sum(similarities)/len(similarities)
        most_similar_to = [provided_search_keywords[i] for i in range(len(provided_search_keywords)) if similarities[i]==similarity_max]
        if len(most_similar_to) >= 1:
            most_similar_to = ";".join(most_similar_to)
        else:
            most_similar_to = ''
            
        # check similarities with respect to article categories
        similarities_category = []
        for ac in article_category_embeddings:
            similarities_category.append(util.cos_sim(ac, summary_embedding).item())
        similarity_category_max = max(similarities_category)
            
        # : For articles with Prioritize = 1 but max_score < 0.3, update Prioritize as -1
        if (similarity_category_max < 0.1):
            prioritize_ind = -1
        
        latest_article.loc[index, 'MAX_SCORE_CATEGORY'] = similarity_category_max
        latest_article.loc[index, 'MAX_SCORE'] = similarity_max
        latest_article.loc[index, 'AVG_SCORE'] = similarity_avg
        latest_article.loc[index, 'Most Relevant Keyword'] = most_similar_to
        latest_article.loc[index, 'Prioritize'] = prioritize_ind
        latest_article.loc[index, 'Contains Keyword'] = contain_keywords
        
    ## Sort by max similarity scores
    latest_article = latest_article.sort_values(by=['Prioritize','MAX_SCORE'], ascending=[False, False])
    latest_article.reset_index(drop=True, inplace=True)
    
    # update archive
    archive_bulk_insert(latest_article)
#    latest_article.to_excel('filter_sort_xq_output_v3.xlsx', index=False)
#    print(latest_article.info())
    
    return latest_article[['Title','Publish Date','Summary','Summary_EN','URL','Contains Keyword','Most Relevant Keyword']]

def generate_newsletter_email_html():
    newsletter_article = filter_sort_articles()
    total_nb_articles = len(newsletter_article)
    newsletter_article = newsletter_article.head(min([nb_articles_selected, total_nb_articles]))
    
    emailbody = """\
    <html>
    <head>
    <style>
    h1 {font-size: 150%}
    p {color: black; font-size: 100%}
    </style>
    </head>
    <body>"""
    
    if not newsletter_article.empty:
        for index, row in newsletter_article.iterrows():
            emailbody = emailbody \
                + "<h1><b><a href="+row['URL']+">"+row['Title']+"</a></b></h1>" + '\n' \
                + "<p style=\"color:grey\"><i>"+row['Publish Date'].strftime('%Y %b %d')+" </i><br>" + '\n' \
                
            if row['Contains Keyword'] != '':
                emailbody = emailbody + "<i><b>Contains Keywords: </b>"+row['Contains Keyword']+"</i></p>" + '\n'
            else:
                emailbody = emailbody + "<i><b>Most Relevant To: </b>"+row['Most Relevant Keyword']+"</i></p>" + '\n'
            
            if pd.isnull(row['Summary_EN']):
                emailbody = emailbody + "<p><i><b>Summary: </b></i>" + row['Summary'] + "</p>" + '\n'
            else:
                emailbody = emailbody + "<p><i><b>Summary (Translation): </b></i>" + row['Summary_EN'] + "</p>" + '\n'
    
            emailbody = emailbody + "<hr>" + '\n'
    emailbody = emailbody + """<p> </p>    
    </body>
    </html>
    """
    
    return emailbody

def send_newsletter(recipients):
    message = MIMEMultipart()
    message["To"] = 'Hack4GoodBASE2023'
    message["From"] = 'Hack4GoodBASE2023'
    message["Subject"] = '[Hack4Good2023] Newsletter '+date.today().strftime('%d %b %Y')
    
    title = '<b> Selected Articles This Week: </b>'
    
    emailbody = generate_newsletter_email_html()
    
    messageText = MIMEText(emailbody, "html")
    message.attach(messageText)
    
    email = 'basehack4good@gmail.com'
    # password = 'urrw avdt ikst xvsl'
    password = 'urrwavdtikstxvsl'

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo('Gmail')
    server.starttls()
    server.login(email,password)
    
    fromaddr = 'basehack4good@gmail.com'
    toaddrs = recipients

    server.sendmail(fromaddr,toaddrs,message.as_string())

    server.quit()
    
    return

# Search Keywords

provided_search_keywords = read_gsheet('Prod_BASEconfig', 'Search Keywords', True)
provided_search_keywords = provided_search_keywords['Keywords'].tolist()

article_category = read_gsheet('Prod_BASEconfig', 'Search Category', True)
article_category = article_category['Article Categories'].tolist()

# Update Frequency etc.

config_param = read_gsheet('Prod_BASEconfig', 'UpdateFreq', False)[0]
nb_days = config_param['UpdateFrequency']
nb_articles_selected = config_param['NbArticlesPerNewsletter']

# newsletter recipients
recipients = read_gsheet('Prod_BASEconfig', 'NewsletterRecipients', True)
recipients = recipients['Email Address'].tolist()

send_newsletter(recipients)
