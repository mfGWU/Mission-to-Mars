
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

def scrape_all():
   # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    news_title, news_paragraph = mars_news(browser)
    #img_url, title = hemisphere(browser)
    hemisphere_image_urls= hemisphere(browser)


     # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemisphere_image_urls": hemisphere(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data

# Set the executable path and initialize the chrome browser in splinter
# executable_path = {'executable_path': 'chromedriver'}
# browser = Browser('chrome', **executable_path)

def mars_news(browser):
# Visit the mars nasa news site - assign the url and instruct the browser to visit it
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # set up the HTML parser
    # # Convert the browser html to a soup object and then quit the browser 
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
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
        #news_title

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
        #news_p
    except AttributeError:
        return None, None

    return news_title, news_p

#### Featured Images -Visit the NASA Mars news site
# ## JPL Space Images Featured Image

def featured_image(browser):
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

    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
        #img_url_rel

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    #img_url

    return img_url

#### 10.3.5 Scrape Mars Data: Mars Facts

# Instead of scraping each row, or the data in each <td />, we're going to 
# scrape the entire table with Pandas' .read_html() function.

def mars_facts():
    # Add try/except for error handling
    try:
      # use 'read_html" to scrape the facts table into a dataframe
      df = pd.read_html('http://space-facts.com/mars/')[0]
      #df.head()

    except BaseException:
        return None
    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    # df.columns=['description', 'value']
    df.set_index('Description', inplace=True)
    #df

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

# Now that we've gathered everything on Robin's list, we can end the automated browsing session.
#browser.quit()

def hemisphere(browser):
# function that will scrape the hemisphere data by using your code from the 
#  Mission_to_Mars_Challenge.py
    # 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []


    # 3. Write code to retrieve the image urls and titles for each hemisphere.

    for x in range(0, 1):
    
        # Parse the HTML - use BeautifulSoup to parse the HTML.
        # It means that BeautifulSoup has taken a look at the 
        # different components and can now access them.
        html = browser.html
        html_soup = soup(html, 'html.parser')
        #Scrape the Title - find the title and extract it from H3 .
        hemisphere_titles = html_soup.find_all('h3')
        #keys2 = ['title']
    
        for title in hemisphere_titles:
            title = title.text
            #print(word)
        
            browser.click_link_by_partial_text(title)
        
            #link_titles.append(word)
        
            html = browser.html
            img_urls = soup(html, 'html.parser')
        
            mars_url = img_urls.find_all("a", string="Sample")

            for link in mars_url:
                if link.has_attr('href'):
                    img_url = link.attrs['href']
                    #print(link.attrs['href'])

                
            #Build the list to hold the images and titles.
            if img_url not in hemisphere_image_urls:
                hemisphere_image_urls.append({'img_url':img_url, 'title':title})
            
            browser.back()

    return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())