from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import os
import requests
from fake_useragent import UserAgent


driver=webdriver.Chrome('chromedriver')
main_url='https://gorkhapatraonline.com/'
driver.get(main_url)

#%%
sleep(10)
#go to business section
business_section=driver.find_element_by_link_text('अर्थ')
business_section.click()
#%%
user_agent=UserAgent()
business_section_url='https://gorkhapatraonline.com/economics'
page=requests.get(business_section_url,headers={'user-agent':user_agent.chrome})

soup=BeautifulSoup(page.content,'lxml')
#%%
a_header=soup.find_all('div',class_='banner-header')
for header in a_header:
    print(header.a.string)
    print(header.a['href'])
#%%
features=soup.find_all('div', class_='feature1')
for feature in features:
    print(feature.h5.text)
    print(feature.a['href'])
#%%
bishesh1=soup.find_all('div',class_='bishesh1')
for b in bishesh1:
    print(b.h5.text)    
    print(b.a['href'])
#%%
middle=soup.find('div',class_='middle')
for a in middle.find_all('a'):
    print(a.h5.text)
    print(a['href'])
#%%
forlist=soup.find('ul', class_='forlist')
for f in forlist.find_all('a'):
    print(f.text)
    print(f['href'])
    
#%%
titles_header=[header.a.string for header in a_header]
links_header=[header.a['href'] for header in a_header]
titles_features=[feature.h5.text  for feature in features]
links_features=[feature.a['href'] for feature in features]
titles_bishesh1=[b.h5.text for b in bishesh1]
links_bishesh1=[b.a['href'] for b in bishesh1]
titles_middle=[a.h5.text for a in middle.find_all('a')]
links_middle=[a['href'] for a in middle.find_all('a')]
titles_forlist=[f.text for f in forlist.find_all('a')]
links_forlist=[f['href'] for f in forlist.find_all('a')]
#%%
all_titles=titles_features+titles_bishesh1+titles_middle+titles_forlist
all_links=links_features+links_bishesh1+links_middle+links_forlist
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