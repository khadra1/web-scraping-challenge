# Automated browser actions
from splinter import Browser

# Parses the HTML
from bs4 import BeautifulSoup
import pandas as pd
import time

# For scraping with Chrome
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    # create mars_data dict that we can insert into mongo
    mars_data = {}
    print("starting scraper")
#####################################################################
    # Scrape the Mars News Site and collect the latest News Title and Paragraph
    # The url we want to scrape
    url_news = 'https://redplanetscience.com'    
     
    # Call visit on our browser and pass the url we want to scrape
    browser.visit(url_news)
    
   # 1 second time delay for error purposes    
    time.sleep(1)

    # Scrape page into soup and create a soup object from the html
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Scrape the Mars News Site and collect the latest News Title and Paragraph Text
    title = soup.find_all('div', class_='content_title')[0].text
    paragraph = soup.find_all('div', class_='article_teaser_body')[0].text


#####################################################################    

    # Scrape the Mars News Site and collect current Featured Mars Image
    # The url we want to scrape
    url_image = 'https://spaceimages-mars.com/'
    
    # Call visit on our browser and pass the url we want to scrape
    browser.visit(url_image)
    
    # 1 second time delay for error purposes    
    time.sleep(1)   

    # Scrape page into soup and create a soup object from the html
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
   
    # Scrape the Mars News Site and collect current Featured Mars Image
    results = soup.find_all('a',class_="fancybox-thumbs")
    imageurls = []
    for result in results:
        imageurls.append(url_image+result['href'])
    
    # Asign the URL string to a variable called featured_image_url
    featured_image_url = url_image+results[0]['href']
    
    
 #####################################################################   

    # Obtain high-resolution images for each hemisphere of Mars
    # The url we want to scrape
    url_facts = 'https://galaxyfacts-mars.com'
    
    # Use Panda's `read_html` to parse the url and scrape all tabular data from page
    tables = pd.read_html(url_facts)

    # Scrape the table containing facts about Mars
    mars_table = tables[0]
   

    # Rename columns and reset index to match example
    mars_table = mars_table.rename(columns={0:'Description', 1:'Mars', 2: 'Earth'})
    mars_table.set_index('Description', inplace=True)
    # Use Pandas to convert the data to a HTML table string.
    mars_html= mars_table.to_html()

#####################################################################

    # Obtain high-resolution images for each hemisphere of Mars 
    # The url we want to scrape
    url_hemi = 'https://marshemispheres.com/'
    
    #Call visit on our browser and pass the url we want to scrape
    browser.visit(url_hemi)
    # 1 second time delay for error purposes    
    time.sleep(1)

    # Scrape page into soup and create a soup object from the html
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    # Scrape the Mars Hemispheres Site and collect title and image urls for high-resolution images for each hemisphere
    results = soup.find_all('div', class_='item')

    # Create empty list for hemisphere title and image results
    hemisphere_image_urls=[]

    # Retrieve each list item
    
    for result in results:
        title = result.find('h3').get_text()
        img_url = result.find('img', class_='thumb')['src']
        img_url = url_hemi + img_url
        hemisphere_image_urls.append({'title': title,'img_url':img_url})


#####################################################################
    # Save all the above data in the empty dict
    mars_data = {'title': title,
    'paragraph': paragraph,
    'featured_image': featured_image_url,
    'mars_table': mars_html,
    'hemisphere_images': hemisphere_image_urls
    }
#####################################################################
    # Quit the browser
    browser.quit()
    return mars_data
