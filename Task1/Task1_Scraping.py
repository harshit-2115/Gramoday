import numpy as np
import pandas as pd
import requests
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver

FROM_DATE = '01-Jan-2020'
TO_DATE = '31-Dec-2020'
url = f'https://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity=24&Tx_State=UP&Tx_District=1&Tx_Market=0&DateFrom=01-Jan-2020&DateTo=31-Dec-2020&Fr_Date={FROM_DATE}&To_Date={TO_DATE}&Tx_Trend=0&Tx_CommodityHead=Potato&Tx_StateHead=Uttar+Pradesh&Tx_DistrictHead=Agra&Tx_MarketHead=--Select--'
driver = webdriver.Chrome('./chromedriver_linux64/chromedriver')
driver.get(url)

df_cols = []
df_rows = []

itr = 0
while(1):
    print(f'Scraping Page:{itr + 1}')
    soup = BeautifulSoup(driver.page_source, 'lxml')
    table = soup.find_all('table', attrs={'class':'tableagmark_new'})[0]
    body = table.find_all('tr')
    table_rows = body[1:]
    if(itr == 0):
        header = body[0]
        for i in header.find_all('th'):
            df_cols.append(i.get_text())
    
    
    for i in range(len(table_rows)):
        row_data = []
        for j in table_rows[i].find_all('td'):
            tmp = j.get_text()
            tmp = str(tmp).strip()
            row_data.append(tmp)
        df_rows.append(row_data)
    
    try:
        driver.find_element_by_xpath('//input[@src="../images/Next.png"]').click()
    except:
        print('Scraping Done')
        driver.close()
        break
    itr = itr + 1
    time.sleep(5)

df = pd.DataFrame(df_rows, columns=df_cols)
df = df.dropna()
df.head()

num_cols = ['Sl no.', 'Min Price (Rs./Quintal)', 'Max Price (Rs./Quintal)', 'Modal Price (Rs./Quintal)']

df[num_cols] = df[num_cols].astype(float) 
df['Price Date'] = pd.to_datetime(df['Price Date'])

df.to_csv('2020_Potato_Agra_Price.csv', index=False)



