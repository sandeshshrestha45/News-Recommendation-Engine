from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import os
import requests
from fake_useragent import UserAgent


driver=webdriver.Chrome('chromedriver')
main_url='https://myrepublica.nagariknetwork.com'
driver.get(main_url)

#%%
#go to business section
sleep(5)
business_section=driver.find_element_by_link_text('ECONOMY')
business_section.click()
#%%
user_agent=UserAgent()
business_section_url='https://myrepublica.nagariknetwork.com/category/economy'
page=requests.get(business_section_url,headers={'user-agent':user_agent.chrome})

soup=BeautifulSoup(page.content,'lxml')
#%%
all_divs=soup.find('div',class_='box categories-list-news')
for a in all_divs.find_all('a'):
    print(a['href'])
for h2 in all_divs.find_all('h2'):
    print(h2.text)
#%%
titles=[h2.text for h2 in all_divs.find_all('h2')]
links=[main_url+a['href'] for a in all_divs.find_all('a')]
sliced_links=links[0:len(links):3]  
#%%
from openpyxl import load_workbook

book=load_workbook('news-english.xlsx')
sheet=book.active

for i in range(len(titles)):
    sheet.append([titles[i],sliced_links[i]])
    
book.save('news-english.xlsx')  
#%%
#handle duplicates
import pandas as pd
file_df = pd.read_excel("news-english.xlsx")
file_df_first_record = file_df.drop_duplicates(subset=["Titles", "Links"], keep="first")
file_df_first_record.to_excel("news-english.xlsx", index=False)
