#!/usr/bin/env python
# coding: utf-8




# Dependencies
from bs4 import BeautifulSoup
import requests
import pandas as pd
from splinter import Browser


def scrape_info():
    
    browser = Browser('chrome')
    mars = {}
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news'



    # Retrieve page with the requests module
    response = requests.get(url)


    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')





    # Examine the results, then determine element that contains sought info
    print(soup.prettify())


    # # NASA Mars News              


    results = soup.find_all('div', class_="slide")
        
    for result in results:
       
        try:     
            title=result.find('div',class_="content_title").a.text
        
            description=result.find('div',class_="rollover_description_inner").text
        
            print("title and descriptions are :") 
            print("-----------------------------")
            if(title and description):
        
                print(title)
                print(description) 
            
        except AttributeError as e:
            print(e)
            
   
    news_title=result.find('div',class_="content_title").a.text
        
    news_p=result.find('div',class_="rollover_description_inner").text

    mars["news_title"] = news_title
    mars["news_paragraph"] = news_p
    print(mars["news_title"], " ",mars["news_paragraph"])


    # # JPL Mars Space Images - Featured Image




    url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    response = requests.get(url)



    browser=Browser("chrome")


    browser.visit(url)

    click_image=browser.find_by_id("full_image")

    click_image.click()


    links_found1 = browser.find_link_by_partial_text('more info')


    links_found1.click()



    soup = BeautifulSoup(browser.html, 'html.parser')


    result=soup.find('figure',class_="lede")


    featured_image_url="https://www.jpl.nasa.gov"+result.a.img["src"]
    featured_image_url
    mars["featured_image"] = featured_image_url
    
    # # Mars Weather

    url="https://twitter.com/marswxreport?lang=en"


    response=requests.get(url)


    soup = BeautifulSoup(response.text, 'html.parser')


    results = soup.find_all('div', class_="js-tweet-text-container")
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


    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


    response=requests.get(url)


    soup=BeautifulSoup(response.text,"html.parser")
    print(soup.prettify())


    results=soup.find_all('div',class_="item")
    results

    hemisphere_image_urls = []
    

    hemisphere={}
    for result in results:
    
        hemisphere['title']=result.find('div',class_="description").h3.text
        hemisphere['img_url']=result.img['src']
        hemisphere_image_urls.append(hemisphere)
    #    print(title)
    #    print(img_url)
    hemisphere_image_urls
    mars["hemisphere"]=hemisphere_image_urls

    return mars