```python
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
```


```python
exec_path={'executable_path': 'chromedriver'}
browser=Browser('chrome', **exec_path, headless=False)
```

###### NASA Mars news


```python
#Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text.
url="https://mars.nasa.gov/news/"
#response=requests.get(url)
browser.visit(url)
```


```python
#create a Beautiful Soup object
html=browser.html
soup=bs(html,'html.parser')
```


```python
new_title=soup.find_all('div', class_='content_title')[1].text
new_title
```




    "NASA's Perseverance Pays Off Back Home"




```python
news_p=soup.find_all('div', class_='article_teaser_body')[0].text
news_p
```




    'Even as the Perseverance rover approaches Mars, technology on board is paying off on Earth.'



##### JPL Mars Space Images - Featured Image


```python
#assign the url string to a variable called `featured_image_url`.
url="https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
response=requests.get(url)
```


```python
# Use splinter to navigate the site and find the image url for the current Featured Mars Image
html=browser.html
soup=bs(html,'html.parser')
```


```python
jpl_img='https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'
img_url=soup.find_all('img')[1]
featured_image_url=jpl_img+img_url['src']
```


```python
featured_image_url
```




    'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space//assets/arrow_down.png'



##### Mars Facts


```python
#Visit the https://space-facts.com/mars page; 
#use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
mars_url="https://space-facts.com/mars/"
mars_df=(pd.read_html(mars_url))[0]
mars_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Equatorial Diameter:</td>
      <td>6,792 km</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Polar Diameter:</td>
      <td>6,752 km</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Mass:</td>
      <td>6.39 × 10^23 kg (0.11 Earths)</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Moons:</td>
      <td>2 (Phobos &amp; Deimos)</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Orbit Distance:</td>
      <td>227,943,824 km (1.38 AU)</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Orbit Period:</td>
      <td>687 days (1.9 years)</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Surface Temperature:</td>
      <td>-87 to -5 °C</td>
    </tr>
    <tr>
      <th>7</th>
      <td>First Record:</td>
      <td>2nd millennium BC</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Recorded By:</td>
      <td>Egyptian astronomers</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Use Pandas to convert the data to a HTML table string.
mars_html_table=mars_df.to_html(header=False, index=False)
mars_html_table
```




    '<table border="1" class="dataframe">\n  <tbody>\n    <tr>\n      <td>Equatorial Diameter:</td>\n      <td>6,792 km</td>\n    </tr>\n    <tr>\n      <td>Polar Diameter:</td>\n      <td>6,752 km</td>\n    </tr>\n    <tr>\n      <td>Mass:</td>\n      <td>6.39 × 10^23 kg (0.11 Earths)</td>\n    </tr>\n    <tr>\n      <td>Moons:</td>\n      <td>2 (Phobos &amp; Deimos)</td>\n    </tr>\n    <tr>\n      <td>Orbit Distance:</td>\n      <td>227,943,824 km (1.38 AU)</td>\n    </tr>\n    <tr>\n      <td>Orbit Period:</td>\n      <td>687 days (1.9 years)</td>\n    </tr>\n    <tr>\n      <td>Surface Temperature:</td>\n      <td>-87 to -5 °C</td>\n    </tr>\n    <tr>\n      <td>First Record:</td>\n      <td>2nd millennium BC</td>\n    </tr>\n    <tr>\n      <td>Recorded By:</td>\n      <td>Egyptian astronomers</td>\n    </tr>\n  </tbody>\n</table>'



##### Mars Hemispheres


```python
#Visit the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres.
usgs_url='https://astrogeology.usgs.gov'
mars_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
#https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg
browser.visit(mars_url)
```


```python
mars_url_html=browser.html
soup=bs(mars_url_html,'html.parser')
```


```python
#Save both the image url string for the full resolution hemisphere image, 
# and the Hemisphere title containing the hemisphere name.
#Use a Python dictionary to store the data using the keys `img_url` and `title` 
mars_hemisphere=soup.select('div.item')
mars_hemisphere
```




    [<div class="item"><a class="itemLink product-item" href="/search/map/Mars/Viking/cerberus_enhanced"><img alt="Cerberus Hemisphere Enhanced thumbnail" class="thumb" src="/cache/images/39d3266553462198bd2fbc4d18fbed17_cerberus_enhanced.tif_thumb.png"/></a><div class="description"><a class="itemLink product-item" href="/search/map/Mars/Viking/cerberus_enhanced"><h3>Cerberus Hemisphere Enhanced</h3></a><span class="subtitle" style="float:left">image/tiff 21 MB</span><span class="pubDate" style="float:right"></span><br/><p>Mosaic of the Cerberus hemisphere of Mars projected into point perspective, a view similar to that which one would see from a spacecraft. This mosaic is composed of 104 Viking Orbiter images acquired…</p></div> <!-- end description --></div>,
     <div class="item"><a class="itemLink product-item" href="/search/map/Mars/Viking/schiaparelli_enhanced"><img alt="Schiaparelli Hemisphere Enhanced thumbnail" class="thumb" src="/cache/images/08eac6e22c07fb1fe72223a79252de20_schiaparelli_enhanced.tif_thumb.png"/></a><div class="description"><a class="itemLink product-item" href="/search/map/Mars/Viking/schiaparelli_enhanced"><h3>Schiaparelli Hemisphere Enhanced</h3></a><span class="subtitle" style="float:left">image/tiff 35 MB</span><span class="pubDate" style="float:right"></span><br/><p>Mosaic of the Schiaparelli hemisphere of Mars projected into point perspective, a view similar to that which one would see from a spacecraft. The images were acquired in 1980 during early northern…</p></div> <!-- end description --></div>,
     <div class="item"><a class="itemLink product-item" href="/search/map/Mars/Viking/syrtis_major_enhanced"><img alt="Syrtis Major Hemisphere Enhanced thumbnail" class="thumb" src="/cache/images/55a0a1e2796313fdeafb17c35925e8ac_syrtis_major_enhanced.tif_thumb.png"/></a><div class="description"><a class="itemLink product-item" href="/search/map/Mars/Viking/syrtis_major_enhanced"><h3>Syrtis Major Hemisphere Enhanced</h3></a><span class="subtitle" style="float:left">image/tiff 25 MB</span><span class="pubDate" style="float:right"></span><br/><p>Mosaic of the Syrtis Major hemisphere of Mars projected into point perspective, a view similar to that which one would see from a spacecraft. This mosaic is composed of about 100 red and violet…</p></div> <!-- end description --></div>,
     <div class="item"><a class="itemLink product-item" href="/search/map/Mars/Viking/valles_marineris_enhanced"><img alt="Valles Marineris Hemisphere Enhanced thumbnail" class="thumb" src="/cache/images/4e59980c1c57f89c680c0e1ccabbeff1_valles_marineris_enhanced.tif_thumb.png"/></a><div class="description"><a class="itemLink product-item" href="/search/map/Mars/Viking/valles_marineris_enhanced"><h3>Valles Marineris Hemisphere Enhanced</h3></a><span class="subtitle" style="float:left">image/tiff 27 MB</span><span class="pubDate" style="float:right"></span><br/><p>Mosaic of the Valles Marineris hemisphere of Mars projected into point perspective, a view similar to that which one would see from a spacecraft. The distance is 2500 kilometers from the surface of…</p></div> <!-- end description --></div>]




```python
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
hemisphere_image_urls
```




    [{'title': 'Cerberus Hemisphere',
      'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'},
     {'title': 'Schiaparelli Hemisphere',
      'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'},
     {'title': 'Syrtis Major Hemisphere',
      'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'},
     {'title': 'Valles Marineris Hemisphere',
      'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'}]




```python

```
