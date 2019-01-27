from bs4 import BeautifulSoup
import urllib3
import pandas as pd
import wget
import time
import os


def parse_html_doc(html):
    return BeautifulSoup(html, 'html.parser')


def parse_html_from_url(url):
    http = urllib3.PoolManager()

    return parse_html_doc(http.request('GET', url).data)


def html_to_df(soup):
    df_data = {
        'title': [],
        'contents': [],
        'city': [],
        'link': [],
        'format': [],
        'date': [],
        'month': [],
        'year': []
    }

    for anchor in soup.findAll('a', href=True):
        parent_t = anchor.find_parent('table')
        
        if parent_t:
            title = parent_t.find_previous_siblings('h2')[0].string
            contents = anchor.string.strip().split('.')[0]
            city = parent_t.attrs['class'][-1]
            link = anchor['href']
            file_format = link.split('.')[-1]
            export_date = link.split('/')[-3]
            m_year = time.strptime(export_date, "%Y-%m-%d")

            # print("Title: {}".format(title))
            # print("Contents: {}".format(contents))
            # print("City: {}".format(city))
            # print("Link: {}".format(link))
            # print("Format: {}".format(file_format))
            # print("Date: {}".format(export_date))
            # print("-----------------------------------------\n")

            if 'visualisations' not in link:
                df_data['title'].append(title)
                df_data['contents'].append(contents)
                df_data['city'].append(city)
                df_data['link'].append(link)
                df_data['format'].append(file_format)
                df_data['date'].append("{}".format(int(time.strftime("%Y%m", m_year))))
                df_data['month'].append("{}".format(time.strftime("%b", m_year).lower()))
                df_data['year'].append("{}".format(int(time.strftime("%Y", m_year))))
    
    return pd.DataFrame(df_data)


def upload_to_bucket(bucket):
    return None


if __name__ == '__main__':
    DATASETS_URL = 'http://insideairbnb.com/get-the-data.html'

    soup = parse_html_from_url(DATASETS_URL)
    
    df = html_to_df(soup)
    df.to_csv('./raw_files.csv')

    latest_listings = df.query('contents == "listings"').sort_values('date', ascending=False).drop_duplicates(['city'])
    latest_listings['filename'] = latest_listings['city'] + "_" + latest_listings['date'] + ".csv"
    latest_listings['path'] = os.getcwd() + "/data/" + latest_listings['city'] + "_" + latest_listings['date'] + "." + latest_listings['format']
    latest_listings.to_csv('downloaded_files.csv')

    for i, row in latest_listings.iterrows():
        try:
            wget.download(row['link'], row['path'])
        except:
            print("\nFailed to download file for city={} and date={}".format(row['city'], row['date']))
            print("Retrying on an older export for the same city...")
            retry_row = df[df.city == row['city']].sort_values(by=['year'], ascending=False).iloc[[1]]
            
            try:
                wget.download(retry_row['link'], retry_row['path'])
            except:
                print("Failed again, skipping {}...\n".format(row['city']))