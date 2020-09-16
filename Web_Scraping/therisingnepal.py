from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import os
import requests
from fake_useragent import UserAgent


driver=webdriver.Chrome('chromedriver')
main_url='https://risingnepaldaily.com/'
driver.get(main_url)

#%%
#go to business section
sleep(5)
business_section=driver.find_element_by_link_text('Business')
business_section.click()
#%%
user_agent=UserAgent()
business_section_url='https://risingnepaldaily.com/business'
page=requests.get(business_section_url,headers={'user-agent':user_agent.chrome})

soup=BeautifulSoup(page.content,'lxml')
#%%
all_divs=soup.find('div',class_='sports-groups')
for a in all_divs.find_all('a'):
    print(a['href'])
    
for p in all_divs.find_all('p',class_='trand'):
    print(p.text)
#%%
all_titles=[p.text for p in all_divs.find_all('p',class_='trand')]
all_links=[a['href'] for a in all_divs.find_all('a')]
#%%
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
