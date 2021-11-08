#!/usr/bin/env python
# coding: utf-8


# Import Libraries
import time
from datetime import datetime
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import pymongo

def scrape_info():
    # Scrape the Data
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #URL Mars News Site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    time.sleep(1)
    # --- create HTML object ---
    html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html, 'html.parser')
    #soup

    #collect the latest News Title and Paragraph Text
    latest_news_title = soup.find("div", class_ = "content_title").text
    #print(latest_news_title)
    news_pgraph=soup.find("div", class_ = "article_teaser_body").text
    #print(news_pgraph)
    # 
    # ### JPL Mars Space Images - Featured Image
    # 
    #URL JPL Mars Space Image
    jpl_mars_url = 'https://spaceimages-mars.com/'
    browser.visit(jpl_mars_url)

    time.sleep(1)
    # --- create HTML object ---
    html = browser.html
    # Create BeautifulSoup object; parse with 'html.parser'
    image_soup = bs(html, 'html.parser')
    #image_soup
    # find the image url to the full size .jpg and save a complete url string for this image
    featured_image = image_soup.find("img", class_ = "headerimage fade-in")
    featured_image_url = jpl_mars_url + featured_image["src"]
    #print(featured_image_url)
    # 
    # ### Mars Facts

    #URL Mars Facts
    marsfacts_url = 'https://space-facts.com/mars/'
    browser.visit(marsfacts_url)

    time.sleep(1)
    # --- create HTML object ---
    html = browser.html
    #html
    # use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    mars_table = pd.read_html(html)
    #mars_table

    mfacts_df = mars_table[0]
    mfacts_df.columns =['Description','Value']
    #mfacts_df

    #Use Pandas to convert the data to a HTML table string.
    mfacts_df.to_html("mars_facts.html",index =False)
    mfacts = mfacts_df.to_html(header=True,index=False)
    #print(mfacts)

    # ### Mars Hemispheres

    # Visit the astrogeology site
    marshems_url = "http://marshemispheres.com/"
    browser.visit(marshems_url)

    time.sleep(1)
    # --- create HTML object ---
    html = browser.html
    # html
    # Create BeautifulSoup object; parse with 'html.parser'
    marshem_soup = bs(html, 'html.parser')
    # marshem_soup

    #link is located in "div" class "description"
    divs_desc = marshem_soup.find_all("div", class_ = "description")
    #divs_desc

    hemis = []
    for h in divs_desc:
        hems_html = h.find("a")["href"]
        hemis.append(hems_html)
    #hemis

    # Create list of dictionaries called hemisphere_image_urls
    hemisphere_image_urls = []

    # Iterate through all URLs saved in variable
    for h in hemis:
    
        mars_hem_url = marshems_url + h
    #print(mars_hem_url)
    
    # Visit to url
        browser.visit(mars_hem_url)
        #time.sleep(1)
    # HTML Object
        html = browser.html

     # Parse HTML with Beautiful Soup
        soup = bs(html, 'html.parser')

    # Find all full resolution image for all Hemisphere URLs
        img_url = soup.find("img", class_ = "wide-image")["src"]
    
    # Find all titles 
        title = soup.find("h2", class_ = "title").text
        hemis_title = title.split(" Enhanced")[0] #removed the enhanced word
        #print(hemis_title)
    
    # Append image&title to the dict
        hemisphere_image_urls.append({"title": hemis_title, "img_url": marshems_url + img_url})

    # Exit Browser
    browser.quit()

    #hemisphere_image_urls

    # 
    #         MARS Data


    #Create Dictionary for all Mars Data
    Mars_Data ={}
    #Append all Scrapped Data
    Mars_Data['latest_news_title'] = latest_news_title
    Mars_Data['news_paragraph'] = news_pgraph
    Mars_Data['featured_image_url'] = featured_image_url
    Mars_Data['mars_facts'] = mfacts
    Mars_Data['mars_hemispheres_urls'] = hemisphere_image_urls

    # Return results
    return Mars_Data

    #Mars_Data
    #Connect to mongoDB
    # conn = 'mongodb://localhost:27017'
    # client = pymongo.MongoClient(conn)

    # #Insert object into MongoDB
    # client.mars_db.marsample_data.insert_one(Mars_Data)




