from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import os
import requests
from fake_useragent import UserAgent


driver=webdriver.Chrome('chromedriver')
main_url='https://thehimalayantimes.com'
driver.get(main_url)

#%%
sleep(20)
#cancel popup dialog
cancel_button=driver.find_element_by_id('onesignal-slidedown-cancel-button')
cancel_button.click()
sleep(5)
#go to business section
business_section=driver.find_element_by_link_text('Business')
business_section.click()
#%%
user_agent=UserAgent()
business_section_url='https://thehimalayantimes.com/category/business'
page=requests.get(business_section_url,headers={'user-agent':user_agent.chrome})

soup=BeautifulSoup(page.content,'lxml')
#%%
all_divs=soup.find('div',class_='col-sm-8')
for div in all_divs.find_all('a'):
    print(div.text)
    print(div['href'])
    
#%%
all_titles=[div.text for div in all_divs.find_all('a')]
all_links=[div['href'] for div in all_divs.find_all('a')]
#%%
from openpyxl import load_workbook

book=load_workbook('news-english.xlsx')
sheet=book.active

for i in range(len(all_titles)):
    sheet.append([all_titles[i],all_links[i]])
    
book.save('news-english.xlsx')    
#%%
#handle duplicates
import pandas as pd
file_df = pd.read_excel("news-english.xlsx")
file_df_first_record = file_df.drop_duplicates(subset=["Titles", "Links"], keep="first")
file_df_first_record.to_excel("news-english.xlsx", index=False)