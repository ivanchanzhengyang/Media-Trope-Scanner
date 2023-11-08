#!/usr/bin/env python
# coding: utf-8

# # Trope media scanner v 1.0

# don't forget to put hyperlinks and stuff

# # Contents

# put in your contents page here

# # 0 - Introduction 

# ## A. What is TVTropes?

# TV Tropes is a wiki website that collects and describes common plot devices, character archetypes, and other storytelling elements. It is a valuable resource for writers, filmmakers, and other storytellers, as well as fans of popular culture who want to learn more about the stories they love. Some examples of tropes that are covered on TV Tropes include [the Hero's Journey](https://tvtropes.org/pmwiki/pmwiki.php/Main/TheHerosJourney), [Chekhov's Gun](https://tvtropes.org/pmwiki/pmwiki.php/Main/ChekhovsGun), and [Coming of Age story](https://tvtropes.org/pmwiki/pmwiki.php/Main/ComingOfAgeStory).

# ## B. Problem Statement

# Identifying tropes in creative works can be a time-consuming and challenging task, especially for long or complex works. This can make it difficult for writers, filmmakers, and other storytellers to identify and use tropes effectively, and to avoid clichés. Additionally, fans of popular culture may have difficulty learning more about the tropes used in their favorite stories.
# 
# A trope scanner can help to solve this problem by automating the process of identifying tropes in creative works. This can save writers, filmmakers, and other storytellers a significant amount of time, and can help them to create more engaging and original stories. Additionally, a trope scanner can make it easier for fans of popular culture to learn more about the tropes used in their favorite stories.
# 
# Here are some specific examples of how a trope scanner can be used:
# - A writer can use a trope scanner to identify and use tropes effectively in their work. For example, a writer could use a trope scanner to find examples of the Hero's Journey trope in popular movies, and then use those examples to inform their own writing.
# - A filmmaker can use a trope scanner to identify and avoid clichés in their films. For example, a filmmaker could use a trope scanner to find examples of the [Deus ex Machina](https://tvtropes.org/pmwiki/pmwiki.php/Main/DeusExMachina) trope, and then avoid using that trope in their own films.
# - A fan of popular culture can use a trope scanner to learn more about the tropes used in their favorite stories. For example, a fan of superhero movies could use a trope scanner to find examples of the [Secret Identity](https://tvtropes.org/pmwiki/pmwiki.php/Main/SecretIdentity) trope, and then learn more about the history and significance of that trope.

# ## C. Goal

# The ultimate aim of this project is to create a bot that can populate a TVTropes wiki article with a serviceable first draft for a new piece of media. To do this, this bot needs to do the following:
# 
# A. Ingest some media <br>
# B. Create a summary of the media <br>
# C. Identify main characters <br>
# D. Identify tropes present in the media <br>
# E. Create sub sections for the tropes <br>
# 
# However, because of time restrictions, this project will only aim to create a multiclass classification model that can identify whether certain tropes are present in a piece of media. The target is an accuracy of above 0.9.
# 
# The tropes to be used as classes are:
# * [insert tropes as needed]
# * [insert tropes as needed]
# * [insert tropes as needed]
# 
# 
# A stretch goal for the project is to initialise an LLM model to generate text for steps B and D in the previously mentioned workflow. 

# <font color = 'red'> Hi Ivan, the above is what I have written for your project goals. PLEASE FEEL FREE TO CHANGE ANY OR ALL OF IT! I just wrote something that I thought was a feasible and still fairly impressive goal for your capstone to give you something to work with. Please do not feel obliged to stick with it if you hate it.</font>

# # 1 - Imports (libraries)

# In[1]:


# Import basic libraries
import pandas as pd
import numpy as np


# In[2]:


# Import scraping libraries
import requests
from bs4 import BeautifulSoup


# In[3]:


# Import regex
import re


# In[4]:


#!pip install matplotlib-venn (uncomment if the module isn't imported)

# Import visualisation libraries
import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import seaborn as sns


# In[5]:


# Added the string module to provide functions and constants for working with strings, such as finding and replacing characters, splitting and joining strings, and converting strings to other types.
import string


# In[6]:


#!pip install selenium (uncomment if not installed)

import time
from selenium import webdriver
from selenium.webdriver.common.by import By


# In[7]:


#Other modules that are used in this notebook

import random
import transformers


# In[8]:


# some display adjustments to account for the fact that we have many columns
# and some columns contain many characters

np.set_printoptions(threshold=np.inf)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 800)


# # 2 - Scraping Episodes

# In[9]:


# base wiki url

wiki_url = 'https://simpsons.fandom.com/wiki/'


# In[10]:


#checking to see if site is up

response = requests.get(wiki_url)
print(response)


# For this case, let's scrape just Season 1 first. We need to see if we can even scrape anything first.

# In[11]:


# list of seasons to scrape

seasons_list = ['Season_1']


# In[12]:


# list of episode urls to scrape

episodes_urls = []

for season in seasons_list:
    url = wiki_url + season
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    episode_table = soup.find('table', class_='wikitable')
    for i, row in enumerate(episode_table.find_all('tr')):
        if i != 0:
            for i, links in enumerate(row.find_all('a')):
                if i == 1:
                    episodes_urls.append(links.get('href'))


# In[13]:


episodes_urls


# According to the wiki there are indeed only 13 episodes in Season 1, so in short it works. Let's just remove the /wiki/ from the front since we have it at the end of our base url.

# In[14]:


episodes_urls = [x[6:] for x in episodes_urls]
episodes_urls


# In[15]:


def scrape_clean(section):
    text = section.get_text()
    text = text.replace('\n','')
    text = text.replace('\t','')
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    return text


# In[16]:


# now to scrape text from each episode page

episode_list = []
full_story = []
wiki_text = {}

for episode in episodes_urls:
    url = wiki_url + episode
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all <h2> elements on the page
    section_headings = soup.find_all("h2")

    # Get the contents
    for i, heading in enumerate(section_headings):
        text = scrape_clean(heading)
        if i == 0:
            episode_title = text
            episode_list.append(episode_title)
            print(episode_title)
            
        
        if text == 'Full Story' or text == 'Story':  
            # i noticed that one episode was missing and it's because 
            # that page called this section story instead of full story
            # hence the second clause
            
            paragraphs = heading.find_all_next("p")
            full_text = ''
            
            for paragraph in paragraphs:
                # Check if a new header is detected and break the loop
                
                if paragraph.find("h2"):
                    break
                
                paragraph_text = scrape_clean(paragraph)
                
                if len(paragraph_text)>0:
                    full_text += ''.join(paragraph_text)
                    
            print(f'Length of full text is {len(full_text)}.')
            full_story.append(full_text)

for key, value in zip(episode_list, full_story):
    wiki_text.update({key:value})


# Going to call one episode just to check how it looks:

# In[17]:


wiki_text['Simpsons Roasting on an Open Fire']


# Seems to work fine, so the scraping of the season was successful.

# In[18]:


# please insert code for turning the dictionary into a dataframe and exporting to csv for future notebooks




# Next step: scraping trope pages.

# # 3 - Scraping Tropes

# This section is a bit more complicated because basically we need to get the full descriptive text of each trope that is present in each episode. Actually that might get pretty intense so maybe instead of doing EVERY trope, we should do the top 10.

# The method for scraping: 
# 1. Access the main TV show recap page
# 2. Find the season(s) for scraping
# 3. Extract the URLs for the seasons to a list
# 4. Iterate through the list to find the top 10 tropes and extract those to a list too 
# 5. Finally, iterate through the trope list and save the text for analysis

# In[19]:


# base tvtropes url
tvt_url = 'https://tvtropes.org'


# In[20]:


# base tv show url

recap_url = 'https://tvtropes.org/pmwiki/pmwiki.php/Recap/TheSimpsons'


# In[21]:


#checking to see if site is up

response = requests.get(recap_url)
print(response)


# In[22]:


# We can use the same seasons list as previously


# The code below is what will load the page... (insert text here)

# In[23]:


driver = webdriver.Chrome()

# Navigate to the webpage
driver.get(recap_url)

# Wait for the page to load
time.sleep(2)

# scroll once to get past the ad
bottom_element = driver.find_element(By.CSS_SELECTOR,'div.folderlabel.toggle-all-folders-button')
bottom_element.location_once_scrolled_into_view

# use selenium to click on the 'open/close all folders' button
driver.find_element(By.CSS_SELECTOR,'div.folderlabel.toggle-all-folders-button').click()

# Use Beautiful Soup to parse the page using the 'lxml' library
soup = BeautifulSoup(driver.page_source, 'lxml')

# Close the browser session (we don't need it any more)
driver.quit()

seasons = soup.find_all('div', class_ = 'folder')


# In[24]:


# empty list of urls to scrape
episodes_urls = []

# iterate through seasons

for season in seasons:
    for episode in season.find_all('a', class_ = 'twikilink'):
        if 'TheSimpsonsS' in str(episode):
            episode_url = episode.get('href')
            print(episode_url)
            episodes_urls.append(episode_url)


# At this point we have the list of every single episode recap page for every season. You can choose to limit the list to fewer seasons by changing the code above or adding additional code below. However for the sake of this example code I'm going to just take 1 link.

# In[25]:


episodes_urls[0]


# In[26]:


# now to find the links for tropes

trope_urls = []
trope_recap = []

# for episode in episodes_urls: # use this for loop if you want to go through multiple episodes
url = tvt_url + episodes_urls[0]
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

trope_list = soup.find_all('a', class_ = 'twikilink')

for trope in trope_list:
    if 'TheSimpsons' not in str(trope):
        trope_url = trope.get('href')
        trope_text = trope.get_text()
        trope_urls.append(trope_url)
        trope_recap.append(trope_text)

        
# Find all 'li' elements
list_items = soup.find_all('li')

for item in list_items:
    # Find the 'a' tag with class 'twikilink'
    desired_tag = item.find('a', class_='twikilink')
    
    if desired_tag:
        
        # Find the text next to the link
        recap_text = item.get_text(strip=True)
        recap_text = recap_text.lstrip(':').strip()
        recap_text = re.findall(r'\: (.*)', recap_text)
        
        trope_recap.append(recap_text)
        


# I fixed the 'noise' you spoke about, but there are some issues with it--I noticed that some of the sub points also have : which leads to the text before that being deleted. To be honest I'm not sure there's a good way around the issue. Kishan might be right and the best way to get this recap text might be to just copy and paste it in..

# In[27]:


# little bit of cleaning to remove duplicates and links to other media

trope_urls = set(trope_urls)
trope_urls = [x for x in trope_urls if 'Main' in x]


# In[28]:


len(trope_urls)


# While we could scrape all, I think it's a lot to do so let's just pick 10 first. I'm going to do it randomly but feel free to choose them manually (based on domain knowledge perhaps).

# In[29]:


trope_urls = random.sample(trope_urls, 10)


# In[41]:


trope_urls


# In[74]:


# now to scrape text from each trope page

trope_list = []
full_desc = []
trope_text = {}

for trope in trope_urls:
    url = tvt_url + trope
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    heading = soup.find('h1')
    trope_name = scrape_clean(heading)
    trope_list.append(trope_name.strip())
    
    sections = soup.find_all('div', class_ = 'article-content retro-folders')
    
    for section in sections:
        paragraphs = section.find_all_next('p')
        full_text = ''

    for paragraph in paragraphs:
        # Check if a new header is detected and break the loop

        if paragraph.find("h2"):
            break

        paragraph_text = scrape_clean(paragraph)

        if len(paragraph_text)>0:
            full_text += ''.join(paragraph_text)

    print(f'Length of full text is {len(full_text)}.')
    full_desc.append(full_text)

for key, value in zip(trope_list, full_desc):
    trope_text.update({key:value})
    


# In[75]:


trope_list


# In[76]:


# Auto-call from trope_list

for trope in trope_list:
    trope_text[trope]


# In[79]:


def print_trope(trope_name):
    print(f'Trope name: {trope_name}')
    print(trope_text[trope_name])


# In[80]:


for trope in trope_list:
    print_trope(trope)


# In[83]:


# Prompt the user to select a trope
trope_name = input('Select a trope: ')

# Print the full description of the selected trope
print(trope_text[trope_name])

