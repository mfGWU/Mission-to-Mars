#!/usr/bin/env python
# coding: utf-8

# In[56]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[57]:


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)


# ## Visit the NASA Mars News Site

# In[58]:


# Visit the mars nasa news site - assign the url and instruct the browser to visit it
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[59]:


# set up the HTML parser
# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[60]:


# Assign the title and summary text to variables we'll reference later.  
# we chained .find onto our previously assigned variable, slide_elem. When we do 
# this, we're saying, "This variable holds a ton of information, so look inside of that 
# information to find this specific data." The data we're looking for is the content title, 
# which we've specified by saying, "The specific data is in a <div /> with a class of 'content_title'."

slide_elem.find("div", class_='content_title')


# In[61]:


# But we need to get just the text, and the extra HTML stuff isn't necessary.
# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[62]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### Featured Images -Visit the NASA Mars news site - JPL Space Images Featured Image

# In[63]:


# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[64]:


# we want to click the full-size image button, we can go ahead and use the id in our code
# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# In[65]:


# We need to click the More Info button to get to the next page
# This brings us to another useful Splinter functionality: the ability to search for 
# HTML elements by text. In the next available cell, try using Splinter's ability to find elements using text.

# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# In[66]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[67]:


# find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# In[68]:


# Use the base URL to create an absolute URL
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# ### 10.3.5 Scrape Mars Data: Mars Facts

# In[69]:


# Instead of scraping each row, or the data in each <td />, we're going to 
# scrape the entire table with Pandas' .read_html() function.

df = pd.read_html('http://space-facts.com/mars/')[0]

df


# In[70]:


df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
df


# In[71]:


df.to_html()


# ### Mars Weather

# In[72]:


# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# In[73]:


# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# In[74]:


# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[75]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[76]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []


# 3. Write code to retrieve the image urls and titles for each hemisphere.


hemispheres = {}

for x in range(0, 1):
    
    # Parse the HTML - use BeautifulSoup to parse the HTML.
    # It means that BeautifulSoup has taken a look at the 
    # different components and can now access them.
    html = browser.html
    html_soup = soup(html, 'html.parser')
    #Scrape the Title - find the title and extract it from H3 .
    hemisphere_titles = html_soup.find_all('h3')
    #keys2 = ['title']
    
    link_titles=[]
    for title in hemisphere_titles:
        title = title.text
        #print(word)
        
        browser.click_link_by_partial_text(word)
        
        #link_titles.append(word)
        
        html = browser.html
        img_urls = soup(html, 'html.parser')
        
        #shit_url = html_soup.find_all('a').get('href')
        mars_url = img_urls.find_all("a", string="Sample")
        #keys1 = ['img_url','img_url','img_url','img_url']
        
        link_img=[]
        for link in mars_url:
            if link.has_attr('href'):
                img_url = link.attrs['href']
                #print(link.attrs['href'])
                #link_img.append(href)
                
        #Build the list to hold the images and titles.
        if href not in hemisphere_image_urls:
            hemisphere_image_urls.append({'img_url':img_url, 'title':title})
            
        browser.back()
#print(hemisphere_image_urls)
#print(link_img)


# In[77]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[55]:


# 5. Quit the browser
browser.quit()


# In[ ]:


cities = ['Tokyo','Los Angeles','New York','San Francisco']
population = [13350000, 18550000, 8400000, 1837442]
city_popu = {}
#print(cities) # see the specific list object this variable refers to

type(city_popu)


# In[ ]:


# initializing lists 
test_keys = ["Rash", "Kil", "Varsha"] 
test_values = [1, 4, 5] 

# using dictionary comprehension 
# to convert lists to dictionary 
#res = {test_keys[i]: test_values[i] for i in range(len(test_keys))} 
res = dict(zip(test_keys, test_values)) 
print(str(res))


# In[ ]:


# initializing lists 
test_keys_ll = ["img_url1", "img_url2", "img_url3"] 
test_values_11 = ["https://www.geeksforgeeks.org/python-convert-two-lists-into-a-dictionary", "https://www.geeksforgeeks.org/python-convert-two-lists-into-a-dictionary", "https://www.geeksforgeeks.org/python-convert-two-lists-into-a-dictionary"] 

# using dictionary comprehension 
# to convert lists to dictionary 
#res = {test_keys[i]: test_values[i] for i in range(len(test_keys))} 
res_11 = dict(zip(test_keys_ll, test_values_11)) 
print(str(res_11))

# res_11 = {test_keys_ll[i]: test_values_11[i] for i in range(len(test_keys_ll))}
# print(res_11)


# In[ ]:


a=[]

result=dict(zip(res_11, res))
print(result)
#type(result)
# for i in range(len(res_11)):
#     a.append(res_11[i], res[i])
    
#     print(a)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




