#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
from splinter import Browser
import time
import pandas as pd
from IPython import get_ipython



# In[2]:


#get_ipython().system('which chromedriver')


# In[3]:


# Choose the executable path to driver
def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

# In[4]:

def scrape():
    browser = init_browser()
    # create mars dict that we can insert into mongo
    mars= {}


#get url
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    html = browser.html


# ## Step 1 - Scraping

# ## Scrape the NASA Mars

# #### Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text

# In[5]:


#get html by BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
#print(soup.prettify())


# In[6]:


#Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text

    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div',class_='rollover_description').text

    mars['news_title'] = news_title
    mars['news_p'] = news_p

    print(news_title)
    print(news_p)


# ## JPL Mars Space Images - Featured Image

# #### Use splinter to navigate the site and find the "full size" image url for the current Featured Mars Image

# In[7]:


#locate image web address
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    image_browser = browser.visit(image_url)


# In[8]:


# #Retrieve image url using Beautifulsoup
# image_html = browser.html
# soup = BeautifulSoup(image_html, 'html.parser')
# image = soup_image.find('div',class_='full_image')
# print(image.prettify())


# In[9]:


    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    image_browser = browser.visit(image_url)
    full_image_elm = browser.find_by_id ('full_image')
    full_image_elm.click()


# In[10]:


#time.sleep(5)
    browser.is_element_present_by_text('more info',wait_time=1)
    more_info_elm = browser.find_link_by_partial_text('more info')
    more_info_elm.click()


# In[11]:


    html = browser.html
    soup = BeautifulSoup(html,'html.parser')


# In[12]:


    image = soup.select_one('figure.lede a img').get('src')
    main_url = 'https://www.jpl.nasa.gov'
    featured_image_url = main_url + image

    mars['featured_image_url'] = featured_image_url

    print(featured_image_url)


# ## Mars Weather from Twitter

# #### Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page

# In[13]:


#use splinder to open twitter
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


# In[14]:


#get the latest tweet
    weather_tweet = soup.find('div', attrs = {"class":"tweet","data-name":"Mars Weather"})
    mars_weather = weather_tweet.find('p', 'tweet-text').get_text()

    mars['mars_weather'] = mars_weather

    print(mars_weather)


# In[15]:


##get the second latest tweet (in case the first one is not about Mars weather)
# weather_tweet = soup.find_all( attrs = {"class":"tweet","data-name":"Mars Weather"})[1]
# mars_weather = weather_tweet.find('p', 'tweet-text').get_text()
#print(mars_weather)


# ## Mars Facts

# #### Visit the Mars Facts webpage, use Pandas to scrape the table containing facts about the planet including Diameter, Mass

# In[16]:


#get url
    url = 'https://space-facts.com/mars/'


# In[17]:


# use pandas to read html
    tables = pd.read_html(url)
    tables


# In[18]:


# pretty the table
    df = tables[1]
    df.columns=['Facts', 'Values']
    df.set_index(['Facts'])


# In[19]:


#Use Pandas to convert the data to a HTML table string
    html_table = df.to_html()
    html_table


# In[20]:


# strip unwanted newlines to clean up the table.
    html_table.replace('\n', '')


# In[21]:


#save html table
    df.to_html('mars_facts_table.html')


# In[22]:


    #get_ipython().system('open table.html')

    mars['mars_facts_table']= html_table

    browser.quit()

    return mars
