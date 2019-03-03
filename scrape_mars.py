#!/usr/bin/env python
# coding: utf-8




# Dependencies
from bs4 import BeautifulSoup
import requests
import pandas as pd
from splinter import Browser
import time


def scrape_info():
    
    browser = Browser('chrome')
    mars = {}
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)
    time.sleep(5)


    # Retrieve page with the requests module
    #response = requests.get(url)


    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(browser.html, 'html.parser')





    # Examine the results, then determine element that contains sought info
    print(soup.prettify())


    # # NASA Mars News              


    results = soup.find_all('div', class_="slide")
    title=[] 
    description=[]   
    for result in results:
       
        try:     
            title.append(result.find('div',class_="content_title").a.text)
        
            description.append(result.find('div',class_="rollover_description_inner").text)
        
            print("title and descriptions are :") 
            print("-----------------------------")
            if(title and description):
        
                print(title)
                print(description) 
            
        except AttributeError as e:
            print(e)
            
   
    news_title=title[0]
        
    news_p=description[0]

    mars["news_title"] = news_title
    mars["news_paragraph"] = news_p
    print(mars["news_title"], " ",mars["news_paragraph"])


    # # JPL Mars Space Images - Featured Image


    jpl_fullsize_url = 'https://photojournal.jpl.nasa.gov/jpeg/'
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)
    time.sleep(5)
    jpl_html = browser.html
    jpl_soup = BeautifulSoup(jpl_html, 'html.parser')
    time.sleep(5)
    featured_image_list=[]
    for image in jpl_soup.find_all('div',class_="img"):
        featured_image_list.append(image.find('img').get('src'))

    feature_image = featured_image_list[0]
    temp_list_1 = feature_image.split('-')
    temp_list_2 = temp_list_1[0].split('/')
    featured_image_url = jpl_fullsize_url + temp_list_2[-1] + '.jpg'
            
    # # Mars Weather

    twitterurl="https://twitter.com/marswxreport?lang=en"

    browser.visit(twitterurl)
    response=requests.get(twitterurl)


    soup2 = BeautifulSoup(browser.html, 'html.parser')


    results = soup2.find_all('div', class_="js-tweet-text-container")
    results



    for result in results:
        mars_weather=result.find('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    print(mars_weather)
    print("<---------------------------------------------------------------------------------->")

    mars["weather"] = mars_weather

    # # Mars Facts

    url="http://space-facts.com/mars/"


    tables = pd.read_html(url)
    tables[0]


    df=tables[0]
    df


    df.columns=['Attributes','Values']
    df
    html_table = df.to_html()
    html_table=html_table.replace('\n', '')
    mars['facts'] = html_table

    df.to_html('table.html')


    # # Mars Hemispheres
    url_hemi = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemi)    
    time.sleep(5)       
    usgs_soup = BeautifulSoup(browser.html, 'html.parser')
    headers = []
    titles = usgs_soup.find_all('h3')  
    time.sleep(5)

    for title in titles: 
      headers.append(title.text)

    images = []
    count = 0
    for thumb in headers:
        browser.find_by_css('img.thumb')[count].click()
        images.append(browser.find_by_text('Sample')['href'])
        browser.back()
        count = count+1

    hemisphere_image_urls = []  #initialize empty list to collect titles
    counter = 0
    for item in images:
        hemisphere_image_urls.append({"title":headers[counter],"img_url":images[counter]})
        counter = counter+1
    # closeBrowser(browser)
    browser.back()
    time.sleep(1)
    mars["hemisphere"]=hemisphere_image_urls
    print(hemisphere_image_urls)

    return mars
if __name__ == "__main__":
    print(scrape_info())