from datetime import date

import pandas as pd

import pygsheets

# google sheets authorization
gc = pygsheets.authorize(service_file='gsheet-from-py-test-3586154cc69e.json')
sh = gc.open('Articles')

def read_gsheet(worksheetname, ReadAsDF):
    wks = sh.worksheet(property='title', value=worksheetname)
    if ReadAsDF:
        return wks.get_as_df()
    else:
        return wks.get_all_records()


def archive_bulk_insert():
    latest_articles = read_gsheet('WebScraping', ReadAsDF=True)
    archives = read_gsheet('Archive', ReadAsDF=True)
    
    latest_articles['label'] = 'new'
    archives['label'] = 'archive'
    
    all_articles = pd.concat([archives, latest_articles[archives.columns]])
    
    all_articles = all_articles.drop_duplicates(subset='Title', keep='first')
    
    all_articles = all_articles[all_articles['label']=='new'].drop('label', axis=1)
    all_articles['Publish Date'] = pd.to_datetime(all_articles['Publish Date'])
    all_articles['Publish Date'] = all_articles['Publish Date'].dt.strftime('%Y-%m-%d %HH:%mm:%ss')
    
    wks_archive = sh.worksheet(property='title', value='Archive')
    
    if not all_articles.empty:
        wks_archive.append_table(all_articles.values.tolist(), overwrite=False)

    return

def archive_bulk_delete():
    archives = read_gsheet('Archive', ReadAsDF=True)
    archives['Publish Date'] = pd.to_datetime(archives['Publish Date']).dt.date
    
    # first record with publish date >= today - 365 days
    first_record = min(archives[archives['Publish Date']>=date.today()-pd.to_timedelta(365, unit='d')].index)
    
    # delete: start from row 2 in google sheet
    # number of records to delete = first_record + 1
    wks_archive = sh.worksheet(property='title', value='Archive')
    wks_archive.delete_rows(2, first_record)

    return

archive_bulk_insert()
archive_bulk_delete()
