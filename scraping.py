
#dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

#setup splinter
executable_path= {'executable_path': ChromeDriverManager().install()}
browser= Browser('chrome', **executable_path, headless=False)


#visit the mars nasa news site
url= 'https://redplanetscience.com'
browser.visit(url)

#optional delay for loading the page
browser.is_element_not_present_by_css('div.list_text', wait_time=1)

#Convert the browser html to a soup object and then quit the browser
html= browser.html
news_soup= soup(html, 'html.parser')
slide_elem= news_soup.select_one('div.list_text')
slide_elem.find('div', class_='content_title')

#use the parent element to find the first 'a' tag adn save it as 'news_title'
news_title= slide_elem.find('div', class_='content_title').get_text()
news_title

#use the parent element to find the paragraph text
news_p= slide_elem.find('div', class_= 'article_teaser_body').get_text()
news_p

browser.quit()

 [markdown]
# ### JPL Space Images Featured Image

#visit url
url= 'https://spaceimages-mars.com'
browser.visit(url)

#find and click the full image button
full_image_elem= browser.find_by_tag('button')[1]
full_image_elem.click()

#parse the resulting html with soup
html= browser.html
img_soup= soup(html, 'html.parser')

#find the relative image url
img_url_rel= img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

#use the base url to create an absolute url
img_url= f'https://spaceimages_mars.com/{img_url_rel}'
img_url

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

df.to_html()

browser.quit()




















