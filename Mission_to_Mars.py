# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)

# Visit the mars nasa news site - assign the url and instruct the browser to visit it
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

# set up the HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')

# Assign the title and summary text to variables we'll reference later.  
# we chained .find onto our previously assigned variable, slide_elem. When we do 
# this, we're saying, "This variable holds a ton of information, so look inside of that 
# information to find this specific data." The data we're looking for is the content title, 
# which we've specified by saying, "The specific data is in a <div /> with a class of 'content_title'."

slide_elem.find("div", class_='content_title')

# But we need to get just the text, and the extra HTML stuff isn't necessary.
# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p

# ### Featured Images -Visit the NASA Mars news site

# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

# we want to click the full-size image button, we can go ahead and use the id in our code
# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# We need to click the More Info button to get to the next page
# This brings us to another useful Splinter functionality: the ability to search for 
# HTML elements by text. In the next available cell, try using Splinter's ability to find elements using text.

# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url

# ### 10.3.5 Scrape Mars Data: Mars Facts
# Instead of scraping each row, or the data in each <td />, we're going to 
# scrape the entire table with Pandas' .read_html() function.

#By specifying an index of 0, we're telling 
#Pandas to pull only the first table it encounters
df = pd.read_html('http://space-facts.com/mars/')[0]
df.head()

#assign columns to the new DataFrame for additional clarity.
df.columns=['description', 'value']

# By using the .set_index() function, we're turning the Description 
# column into the DataFrame's index. inplace=True means that the 
#updated index will remain in place, without having to reassign 
# the DataFrame to a new variable.
df.set_index('description', inplace=True)
df

#  Pandas also has a way to easily convert our 
# DataFrame back into HTML-ready code using the .to_html() function
df.to_html()

# Now that we've gathered everything on Robin's list, 
# we can end the automated browsing session.
browser.quit()

