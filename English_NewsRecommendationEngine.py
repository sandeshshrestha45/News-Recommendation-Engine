# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 16:10:56 2020

@author: sandesh
"""

import pandas as pd
import streamlit as st 
import re

news = pd.read_excel("news-english.xlsx")
pd.set_option('display.max_rows',None)
pd.set_option('display.max_colwidth', -1) #display complete(non-truncated) content inside a cell

def display_news_containing_keyword(keyword):
    news_headline=news[news['Titles'].str.contains(keyword, na=False, flags=re.IGNORECASE, regex=True)]
    return(news_headline)

news['Titles']=news['Titles'].str.strip()
from sklearn.feature_extraction.text import TfidfVectorizer


tfv = TfidfVectorizer(min_df=3,  max_features=None, 
            strip_accents='unicode', analyzer='word',token_pattern=r'\w{1,}',
            ngram_range=(1, 3),
            stop_words = 'english')

# Filling NaNs with empty string
news['Titles'] = news['Titles'].fillna('')


# Fitting the TF-IDF on the 'Titles' text
tfv_matrix = tfv.fit_transform(news['Titles'])


from sklearn.metrics.pairwise import sigmoid_kernel

# Compute the sigmoid kernel
sig = sigmoid_kernel(tfv_matrix, tfv_matrix)


# Reverse mapping of indices and news titles
indices = pd.Series(news.index, index=news['Titles']).drop_duplicates()

number = st.sidebar.number_input("Number of Recommendations",1,10000000000)

def give_rec(headline,number=number,sig=sig):
    # Get the index corresponding to original_title
    idx = indices[headline]

    # Get the pairwsie similarity scores 
    sig_scores = list(enumerate(sig[idx]))

    # Sort the news titles 
    sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)
    number_of_recs=number
    # Scores of the 10 most similar news
    sig_scores = sig_scores[1:number_of_recs+1]

    # News title indices
    news_indices = [i[0] for i in sig_scores]

    # Top 10 most similar news
    return news['Titles'].iloc[news_indices],news['Links'].iloc[news_indices]

    

def main():
    st.title("EI Maven")
    html_temp = """
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;">News Recommendation Engine (English) </h2>
    </div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)
    keyword = st.text_input("Enter Headline Keyword:","Type Here")
    result=""
    if st.button("Display Search Results"):
        result=display_news_containing_keyword(keyword)
        st.table(result)
       
    headline = st.text_input("Enter Headline for Recommendation:","Type Here")
    result2=""
    if st.button("Display Recommended News"):
        result2=give_rec(headline)
        result2_df=pd.DataFrame(result2)
        transposed_result2_df=result2_df.T
        st.table(transposed_result2_df)   
        
    #copyright
    if st.sidebar.button("©2020,Sandesh Shrestha"):
        st.sidebar.balloons()
        
if __name__=='__main__':
    main()