
#dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    #Initiate headless driver for deployment
    executable_path= {'executable_path': ChromeDriverManager().install()}
    browser= Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph= mars_news(browser)
    mars_hemi_info= hemisphere_info(browser)

    #run all scraping functions and store results in a dictionary
    data= {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": mars_hemi_info,
        "last_modified": dt.datetime.now()
    }
    #stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    #scrape mars news
    #visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    #optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #Convert the browser html to a soup object and then quit the browser
    html= browser.html
    news_soup= soup(html, 'html.parser')

    #add try/except for error handling
    try:
        slide_elem= news_soup.select_one('div.list_text')

        #use the parent element to find the first "a" tag and save it
        news_title= slide_elem.find('div', class_='content_title').get_text()

        #use the parent element to find the paragraph text
        news_p= slide_elem.find('div', class_= 'article_teaser_body').get_text()
        
    except AttributeError: 
        return None, None
    
    return news_title, news_p

def featured_image(browser):
    #visit url
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    #find and click the full image button
    full_image_elem= browser.find_by_tag('button')[1]
    full_image_elem.click()

    #parse the resulting html with soup
    html= browser.html
    img_soup= soup(html, 'html.parser')

    try:
        #find the relative image url
        img_url_rel= img_soup.find('img', class_='fancybox-image').get('src')
        
    except AttributeError:
        return None

    #use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    
    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes= "table table-striped")

def hemisphere_info(browser):
    #Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)

    #Create a list to hold the images and titles.
    hemisphere_image_urls = []

    #Write code to retrieve the image urls and titles for each hemisphere.
    #establish splinter search params
    links= browser.find_by_css('a.product-item img')

    #loop through html to retrive image & title
    for index in range(len(links)):

        #find/select image via elements
        browser.find_by_css('a.product-item img')[index].click()
        s= browser.links.find_by_text('Sample').first

        #create variables for scraping targets
        href= s['href']
        text= browser.find_by_css('h2.title').text

        #create empty dict, assign targets, append to dict
        hemisphere= {}
        hemisphere['img_url']= href
        hemisphere['title']= text
        hemisphere_image_urls.append(hemisphere)
        browser.back()
    return hemisphere_image_urls

if __name__ == "__main__":
    #if running as script, print scraped data
    print(scrape_all())




















