# import requests
# from bs4 import BeautifulSoup
# from requests_html import HTMLSession

# url = "https://turbo.az"

# with HTMLSession() as s:

#     response = s.get(url, headers=HEADERS)
#     response.html.render()

#     soup=BeautifulSoup(response.content,'html.parser')

# products_container = soup.find('div', attrs={'class':'products-container'})


# print(products_container.prettify())

# car_divs=soup.find_all('div', attrs={'class':'products-i'}, recursive=True, limit = 1000)
# print(len(car_divs))

# links=[]

# for car_div in car_divs:
#     link = car_div.select('a.products-i__link')[0].get('href')
#     links.append(link)

# print(len(links))


from bs4 import BeautifulSoup
import time
from selenium import webdriver
import pandas as pd 


# PAUSE_TIME = 0.5

# HEADERS = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
# }

def render_page(url):
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get(url)
    height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script(f"window.scrollTo(0, {height/2})") 
    # time.sleep(PAUSE_TIME)
    driver.execute_script(f"window.scrollTo(0, {height})") 
    # time.sleep(PAUSE_TIME)
    # height = driver.execute_script("return document.body.scrollHeight")
    # driver.execute_script(f"window.scrollTo(0, {height})")
    r = driver.page_source
    
    return r




'''PREMIUM PRODUCTS'''
# url = "https://turbo.az"
# r = render_page(url)
# soup = BeautifulSoup(r, "html.parser")

# premium_products = soup.find('div', attrs={'class':'products products--featured'})
# premium_products_list = premium_products.find_all('div', attrs={'class':'products-i'})
# print(len(premium_products_list))
# premium_links=[]
# for product in premium_products_list:
#     try:
#         link = url + product.find('a', attrs={'class':'products-i__link'}).get('href')
#         premium_links.append(link)
#     except:
#         pass
# # print(premium_links)
# print(f"Length of premium links: {len(premium_links)}")


'''RECENT PRODUCTS'''

# url = "https://turbo.az/autos?page="
# recent_links=[]
# for page_index in range(1, 100):
#     r = render_page(url+str(page_index))
#     soup = BeautifulSoup(r, "html.parser")
#     recent_products = soup.find_all('div', attrs={'class':'products'})[2]
#     recent_products_list = recent_products.find_all('div', attrs={'class':'products-i'})

#     for product in recent_products_list:
#         try:
#             link = url + product.find('a', attrs={'class':'products-i__link'}).get('href')
#             recent_links.append(link) 
#         except:
#             pass

# data = pd.Series(recent_links)
# data.to_csv('recent_links.csv')

# print(f"Length of recent links: {len(recent_links)}")

'''GETTING CAR PROPERTIES'''
# url = "https://turbo.az/autos/7020051-lada-vaz-2107"

# r = render_page(url)
# soup = BeautifulSoup(r, "html.parser")

# properties = soup.find_all('div', attrs={'class':'product-properties__i'})
# print(properties[0].prettify())

# for property in properties:
#     property_name = property.find('label', attrs={'class':'product-properties__i-name'}).text
#     property_value = property.find('span', attrs={'class':'product-properties__i-value'}).text

#     print(f"label: {property_name}\nvalue: {property_value}\n")


# description = soup.find('div', attrs={'class':'product-description__content js-description-content'}).text

# # print(description.text)

# price = soup.find('div', attrs={'class':'product-price__i product-price__i--bold'}).text

def get_all_properties(url):
    all_properties={"url":url}
    r = render_page(url)
    soup = BeautifulSoup(r, "html.parser")
    properties = soup.find_all('div', attrs={'class':'product-properties__i'})
    for property in properties:
        property_name = property.find('label', attrs={'class':'product-properties__i-name'}).text
        property_value = property.find('span', attrs={'class':'product-properties__i-value'}).text
        all_properties.update({property_name:property_value})
        

    
    description = soup.find('div', attrs={'class':'product-description__content js-description-content'}).text
    if description:
        all_properties.update({"description":description})
    else:
        all_properties.update({"description":None})

    # print(description.text)
    price = soup.find('div', attrs={'class':'product-price__i product-price__i--bold'}).text    
    all_properties.update({"price":price})

    return all_properties

links = pd.read_csv('recent_links.csv').iloc[:,0].tolist()

data =  [get_all_properties(links[0]), get_all_properties(links[1])]

turbo = pd.DataFrame(data)
turbo.to_csv('turbo1.csv')
print(turbo)
# for url in links.iloc[:,0].tolist():
#     all_properties = fill_columns(url)
#     print(all_properties)

