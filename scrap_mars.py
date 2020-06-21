# Dependencies
import time
import pandas as pd
import requests as req
from bs4 import BeautifulSoup as bs
from splinter import Browser


def init_browser(): 
 #pointing to the directory where chromedriver exists
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # Visit Nasa news url through splinter module
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    # html = browser.html

    # Parse HTML with Beautiful Soup
    html = browser.html
    soup = bs(html, 'html.parser')
    print(soup.prettify())

    # Extract article title and paragraph text
    article = soup.find("div", class_='list_text')
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_ ="article_teaser_body").text

    #print value
    print(news_title)
    print(news_p)



    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(featured_image_url)


    # HTML Object 
    html_image = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html_image, "html.parser")
    soup

    # Scrape the URL
    image= soup.body.find('article', class_='carousel_item')

    #link can be found in a element 
    link = image.find('a')

    #selecting the image href
    href = link['data-fancybox-href']

    #base uurl
    image_url = 'https://www.jpl.nasa.gov'

    #creating full url 
    featured_image_url = image_url + href

    #printing full url
    print(featured_image_url)


    # Visit Twitter url for latest Mars Weather
    tweet_url = "https://twitter.com/marswxreport?lang=en"

    browser.visit(tweet_url)
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
    soup.prettify()

    mars_weather = soup.body.find('div')
    print(mars_weather)

    # Visit Mars Facts webpage for interesting facts about Mars
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    html = browser.html

    # Use Pandas to scrape the table containing facts about Mars
    table = pd.read_html(facts_url)


    mars_facts = table[0]

    # Rename columns
    mars_facts.columns = ['Description','Value']

    # Reset Index to be description
    mars_facts.set_index('Description', inplace=True)
    mars_facts

    # Use Pandas to convert the data to a HTML table string
    mars_html = mars_facts.to_html(classes = 'table table-striped')
    print(mars_html)


    # Visit USGS webpage for Mars hemispehere images
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, "html.parser")

    # Create dictionary to store titles & links to images
    hemisphere_image_urls = []

    # Retrieve all elements that contain image information
    results = soup.find("div", class_ = "result-list" )
    hemispheres = results.find_all("div", class_="item")

    # Iterate through each image
    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup = bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": image_url})

    # Print image title and url
    print(hemisphere_image_urls)


      # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_facts,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    #close browser after scraping 
    browser.quit()

    #return results 
    return mars_data

if __name__ == '__main__':
    scrape()
