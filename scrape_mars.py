import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser

def init_browser():
    # Define executable path and browser for splinter
    executable_path = {'executable_path':'/chromedriver/chromedriver.exe'}
    return Browser('chrome',**executable_path, headless=False)

def scrape():
    browser = init_browser

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    # Get a handle on the URL with splinter using a wait_time to allow for all results to come through
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    browser.visit(url)

    # Assign the splinter handle to an 'html' object and parse it with BeautifulSoup
    html = browser.html
    soup = bs(html,'lxml')

    # Retrieve the most recent headlines in the page
    headlines = soup.find('div', class_='list_text')

    # Retrieve the most recent headline title and paragraph text
    news_title = headlines.find('div', class_='content_title').a.text
    news_p = headlines.find('div', class_='article_teaser_body').text

    # URL of page to be scraped
    url_image = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # Get a handle on the URL with splinter using a wait_time to allow for all results to come through
    browser.is_element_present_by_css("section.primary_media_feature", wait_time=0.5)
    browser.visit(url_image)

    # Assign the splinter handle to an 'html' object and parse it with BeautifulSoup
    html_image = browser.html
    image_soup = bs(html_image,'lxml')

    # Retrieve the URL for the featured image
    featured_image_url =image_soup.find('footer').find('a', class_='button')['data-fancybox-href']
    featured_image_url = featured_image_url.strip('/')
    featured_image_url = f'https://www.{featured_image_url}'

    # URL of page to be scraped
    mars_twitter = 'https://twitter.com/marswxreport?lang=en'

    # Get a handle on the URL with splinter using a wait_time to allow for all results to come through
    browser.is_element_present_by_tag("article", wait_time=1)
    browser.visit(mars_twitter)

    # Assign the splinter handle to an 'html' object and parse it with BeautifulSoup
    html_twitter = browser.html
    twitter_soup = bs(html_twitter,'lxml')

    # Retrieve the text from the most recent twit
    spans = twitter_soup.find_all('span')

    mw_twits = []
    for span in spans:
        if (span.text and span.text.startswith('InSight')):
            mw_twits.append(span.text)
            
    mars_weather = mw_twits[0]

    # URL of page to be scraped
    mars_facts = 'https://space-facts.com/mars/'

    # Retrieve table data into pandas and convert into a dataframe
    scraped_tables = pd.read_html(mars_facts)

    # Retrieve the first table of those scraped from the URL
    table = scraped_tables[0]

    # Convert the data into a HTML string
    html_table_string = table.to_html(header=False, index=False)

    # URL of page to be scraped
    hem_urls = ['https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced',
            'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced',
            'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced',
            'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced']

    # Retrieve image URLs and hemisphere name for each hemisphere and add them to a list
    hemisphere_image_urls = []

    for hem in hem_urls:
        # Get a handle on the URL with splinter using a wait_time to allow for all results to come through
        browser.is_element_present_by_css("dl dd", wait_time=0.5)
        browser.visit(hem)
        
        # Assign the splinter handle to an 'html' object and parse it with BeautifulSoup
        hem_html = browser.html
        hem_soup = bs(hem_html,'lxml')
        
        # Retrieve the image URL and hemisphere title
        img_url = hem_soup.find('div', class_='content').a['href']
        title = hem_soup.find('h2', class_='title').text
        
        # Modify the title to how only the name of the Hemisphere
        title = title.replace('Enhanced',"")
        
        # Create a dictionary
        dict_hem = {"title":title, "img_url": img_url}
        
        # Add the dictionary to the hemisphere_imare_urls list
        hemisphere_image_urls.append(dict_hem)

    scraped_data = {'news_title': news_title,
                    'news_p': news_p,
                    'featured_image_url': featured_image_url,
                    'mars_weather': mars_weather,
                    'html_table_string': html_table_string,
                    'hemisphere_image_urls':hemisphere_image_urls}
    
    return scraped_data