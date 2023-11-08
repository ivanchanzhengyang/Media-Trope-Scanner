#!/usr/bin/env python
# coding: utf-8

# In[1]:


#importing scripts

import streamlit as st
from bs4 import BeautifulSoup
import requests


# In[2]:


# Function to scrape TV Tropes for trope information
def scrape_tvtropes(trope_name):
    url = f"https://tvtropes.org/pmwiki/pmwiki.php/Main/{trope_name}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    trope_description = soup.find("div", class_="page-content").text
    return trope_description

# Streamlit app
st.title("Trope Scanner")

trope_name = st.text_input("Enter a trope name:")
if trope_name:
    try:
        trope_description = scrape_tvtropes(trope_name)
        st.write("Trope Description:")
        st.write(trope_description)
    except:
        st.error("Trope not found. Please enter a valid trope name.")

