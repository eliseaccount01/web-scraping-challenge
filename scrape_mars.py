#!/usr/bin/env python
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests
from time import sleep


def scrape():

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)


    url_articles = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'


    browser.visit(url_articles)


    #Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(browser.html, 'html.parser')

    #locate title of first article 
    article_title = soup.find(class_='content_title').a.get_text()


    #locate body of article above 
    article_body = soup.find(class_='article_teaser_body').get_text()


    #setting up url to JPL images 
    url_image = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'


    #setting up browser and clicking link 
    browser.visit(url_image)
    link = browser.find_by_css('.articles .fancybox').first
    link.click()

    # Wait for the page load after clicking the link
    sleep(2)


    #Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(browser.html, 'html.parser')


    #locate BIG image photo
    featured_image = soup.find(class_='fancybox-inner').find('img')['src']
    featured_image


    #make url to LARGE image
    large_image_url = f'https://www.jpl.nasa.gov{featured_image}'


    #scrape from twitter 
    url_twitter = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_twitter)
    soup = bs(browser.html, 'html.parser')


    mars_weather = soup.find(class_='tweet-text').get_text()
    mars_weather


    #finding Mars facts 
    facts_url = 'https://space-facts.com/mars/'
    facts_table = pd.read_html(facts_url)
    mars_facts_table = facts_table[1].to_html()


    url_mars_photo = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


    browser.visit(url_mars_photo)
    soup = bs(browser.html, 'html.parser')

    #create empty list 
    photo_pg_links=[]
    photo_links_and_titles=[]


    for link in soup.find_all(class_='item'):
        photo_pg_links.append('https://astrogeology.usgs.gov' + link.a.get('href'))



    for photo in photo_pg_links:
        browser.visit(photo)
        
        #make soup for each page 
        pg_soup = bs(browser.html,'html.parser')
        
        photo_title = pg_soup.find(class_='content').find(class_='title').get_text()
        
        img_url = pg_soup.find(text= 'Original').parent.get('href')
        
        photo_links_and_titles.append({'title':photo_title, 
                                    'img_url': img_url})

    photo_links_and_titles

    return {'article_title': article_title,
            'article_body': article_body,
            'large_image_url': large_image_url,
            'mars_weather':mars_weather,
            'mars_facts_table': mars_facts_table,
            'photo_links_and_titles': photo_links_and_titles}