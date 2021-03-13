#!/usr/bin/env python
# coding: utf-8
# import splinter beautifulSoup and pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
    # excutable_path 
    executable_path = { "executable_path": ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser) 

    data = {
     "new_title": news_title,
     "news_paragraph": news_paragraph,
     "featured_image": featured_image(browser),
     "facts": mars_facts(),
     "hemispheres": hemispheres(browser)
        
    }
    browser.quit()
    return data
    

# NASA Mars News
def mars_news(browser):
    # Visit the NASA mars news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    # Convert the browser html to a soup object and then quit the browser
    new_soup = soup(html, 'html.parser')
    
    try:
        slide_element = new_soup.select_one("ul.item_list li.slide")
        # news title 
        news_title = slide_element.find("div", class_="content_title").get_text()
        print(news_title)

        new_paragraph = slide_element.find("div", class_="article_teaser_body").get_text()
        print(new_paragraph)
    except:
        return None, None

    return news_title, new_paragraph


def featured_image(browser):
    # # feature image
    url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(url)
    html = browser.html
    new_soup = soup(html, 'html.parser')
    
    try:
        full_image_element = new_soup.find("a", class_="showimg fancybox-thumbs")
    except:
        return None
    
    image_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{full_image_element["href"]}'

    return image_url
    
def mars_facts():
    # # Mars Fact

    df = pd.read_html("https://space-facts.com/mars/")[0]
    df.columns=["Description", "Mars"]
    df.set_index("Description", inplace=True)

    return df.to_html(classes="table table-striped")

def hemispheres(browser):
    # # # Hemisphere 
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)


    hemisphere_image_urls = []

    # First get a list of all the hemisphere
    links = browser.find_by_css("a.product-item h3")

    for index in range(len(links)):
        hemisphere = {}

        browser.find_by_css("a.product-item h3")[index].click()

        # Next is find the sample image anchor tag and extract the href 
        try: 
            sample_element = browser.links.find_by_text("Sample").first
            title = browser.find_by_css("h2.title").text
            link = sample_element["href"]

            hemisphere["title"] = title
            hemisphere["link"] = link

            hemisphere_image_urls.append(hemisphere)
            browser.back()
        except:
            return None

        

    return hemisphere_image_urls
    
    






























