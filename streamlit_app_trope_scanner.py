#!/usr/bin/env python
# coding: utf-8

# In[3]:


#importing scripts

import streamlit as st
from bs4 import BeautifulSoup
import requests


# In[4]:


# Function to scrape TV Tropes for trope information
def scrape_tvtropes(trope_name):
    base_url = "https://tvtropes.org/pmwiki/pmwiki.php/Main/"
    url = base_url + trope_name

    try:
        page = requests.get(url)
        page.raise_for_status()
        soup = BeautifulSoup(page.content, "html.parser")
        trope_description = soup.find("div", class_="page-content").text
        return trope_description
    except requests.exceptions.HTTPError as e:
        st.error(f"HTTP error: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Streamlit app
st.title("Trope Scanner")

trope_name = st.text_input("Enter a trope name:")
if trope_name:
    trope_description = scrape_tvtropes(trope_name)
    if trope_description:
        st.write("Trope Description:")
        st.write(trope_description)
    else:
        st.warning("Trope not found. Please enter a valid trope name.")

