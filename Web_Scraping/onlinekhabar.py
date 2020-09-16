from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import os
import requests
from fake_useragent import UserAgent


driver=webdriver.Chrome('chromedriver')
main_url='https://www.onlinekhabar.com'
driver.get(main_url)
#%%
sleep(10)
#extend the sections
icon_hamburger=driver.find_element_by_xpath('//*[@id="primary-menu"]/li[1]')
icon_hamburger.click()
sleep(5)
#go to business section
business_section=driver.find_element_by_link_text('विजनेश')
business_section.click()
#%%
user_agent=UserAgent()
business_section_url='https://www.onlinekhabar.com/business'
page=requests.get(business_section_url,headers={'user-agent':user_agent.chrome})

soup=BeautifulSoup(page.content,'lxml')
#%%
a_large=soup.find_all('a',class_='title__large')
for large in a_large:
    print(large.string)
    print(large['href'])
    
#%%
a_medium=soup.find_all('a',class_='title__medium')
for medium in a_medium:
    print(medium.string)
    print(medium['href'])
    
#%%
a_regular=soup.find_all('div',class_='post__heading')
for regular in a_regular:
    print(regular.a.string)    
    print(regular.a['href'])
#%%
titles_large=[large.string for large in a_large]    
links_large=[large['href'] for large in a_large]
titles_medium=[medium.string for medium in a_medium]    
links_medium=[medium['href'] for medium in a_medium]
titles_regular=[regular.a.string for regular in a_regular]    
links_regular=[regular.a['href'] for regular in a_regular]
#%%%
all_titles=titles_large+titles_medium+titles_regular
all_links=links_large+links_medium+links_regular

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