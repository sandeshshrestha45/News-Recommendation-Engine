from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import os
import requests
from fake_useragent import UserAgent


driver=webdriver.Chrome('chromedriver')
main_url='https://nagariknews.nagariknetwork.com'
driver.get(main_url)

#%%
sleep(5)
#extend the sections
icon_hamburger=driver.find_element_by_xpath('//*[@id="masthead"]/div[1]/div[1]/button')
icon_hamburger.click()
sleep(5)
#go to business section
sleep(5)
business_section=driver.find_element_by_link_text('अर्थ')
business_section.click()
#%%
user_agent=UserAgent()
business_section_url='https://nagariknews.nagariknetwork.com/economy'
page=requests.get(business_section_url,headers={'user-agent':user_agent.chrome})

soup=BeautifulSoup(page.content,'lxml')
#%%
all_divs=soup.find('div',class_='list-group list-layout')
for h1 in all_divs.find_all('h1'):
    print(main_url+h1.a['href'])
    print(h1.text)
#%%
all_titles=[h1.text for h1 in all_divs.find_all('h1')]
all_links=[main_url+h1.a['href'] for h1 in all_divs.find_all('h1')]
#%%
from openpyxl import load_workbook

book=load_workbook('news.xlsx')
sheet=book.active

for i in range(len(all_titles)):
    sheet.append([all_titles[i],all_links[i]])
    
book.save('news.xlsx')
#%%
#handle duplicates
import pandas as pd
file_df = pd.read_excel("news.xlsx")
file_df_first_record = file_df.drop_duplicates(subset=["Titles", "Links"], keep="first")
file_df_first_record.to_excel("news.xlsx", index=False)
