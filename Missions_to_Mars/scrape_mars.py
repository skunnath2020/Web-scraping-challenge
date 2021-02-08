# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
import pandas as pd
from splinter import Browser
from flask import Flask, render_template, redirect
from webdriver_manager.chrome import ChromeDriverManager
# from flask_pymongo import PyMongo
import os
import time
def init_browser()
    exec_path={'executable_path': 'chromedriver'}
    return Browser('chrome', **exec_path, headless=False)


def scrape():
    # NASA Mars news

    #Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text.
    url="https://mars.nasa.gov/news/"
    #response=requests.get(url)
    browser.visit(url)

    #create a Beautiful Soup object
    html=browser.html
    soup=bs(html,'html.parser')

    news_title=soup.find_all('div', class_='content_title')[1].text

    news_p=soup.find_all('div', class_='article_teaser_body')[0].text

    ##### JPL Mars Space Images - Featured Image


    #assign the url string to a variable called `featured_image_url`.
    url="https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    response=requests.get(url)

    # Use splinter to navigate the site and find the image url for the current Featured Mars Image
    html=browser.html
    soup=bs(html,'html.parser')


    jpl_img='https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'
    img_url=soup.find_all('img')[1]
    featured_image_url=jpl_img+img_url['src']

    ##### Mars Facts

    #Visit the https://space-facts.com/mars page; 
    #use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    mars_url="https://space-facts.com/mars/"
    mars_df=(pd.read_html(mars_url))[0]



    #Use Pandas to convert the data to a HTML table string.
    mars_html_table=mars_df.to_html(header=False, index=False)

    ##### Mars Hemispheres

    #Visit the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres.
    usgs_url='https://astrogeology.usgs.gov'
    mars_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    #https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg
    browser.visit(mars_url)

    mars_url_html=browser.html
    soup=bs(mars_url_html,'html.parser')

    #Save both the image url string for the full resolution hemisphere image, 
    # and the Hemisphere title containing the hemisphere name.
    #Use a Python dictionary to store the data using the keys `img_url` and `title` 
    mars_hemisphere=soup.select('div.item')

    #Use a Python dictionary to store the data using the keys `img_url` and `title` 
    hemisphere_image_urls=[]
    for hs in mars_hemisphere:
        #get title 
        title=hs.find('h3').text.replace(' Enhanced', '')
         #get image link by browsing to the page "/search/map/Mars/Viking/cerberus_enhanced"
        mars=hs.find('div', class_='description')
        mars_url=mars.a['href']
        #combine the urls and bring up the full size image page
        browser.visit(usgs_url+mars_url)
        img_html=browser.html
        soup=bs(img_html,'html.parser')
        #scrape the full image link
        img=soup.find('a', text='Sample')
        image_link=img['href']
        #Append the key and values as list of dictionaries
        hemisphere_image_urls.append({'title': title, 'img_url': image_link})
        #get back to the previous page
        browser.back()
    browser.quit()
    # construct and return the Mars dictionary
    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "fact_table": str(mars_html_table),
        "hemisphere_images": hemisphere_image_urls
    }
    return mars_dict