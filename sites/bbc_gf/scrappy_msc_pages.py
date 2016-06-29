from bs4 import BeautifulSoup
import json
import requests
import os, csv
import scrape_uni_writer as prep

headers = {'User-agent': 'Mozilla/5.0'}
beebgf = 'http://www.bbcgoodfood.com/search/recipes?query=#page='
# note for page=14 plus works but below has to be page=09, page=012
# range page= to page=647
bbj = 'http://www.bbcgoodfood.com/search_api_ajax/search/recipes?page='
num_max = 647
beeb_end= '&path=/search/node'

meals = {}
meal_pages={}
meal_own_sites={}

# Got to site
#site = requests.get(bbj, headers=headers)
#print site.raise_for_status()
#print site.status_code
#print site.raw
#print site.text

#data = json.load('jsontest.json')

#with open(site) as data_file:    
#    data = json.load(data_file)

#print data

# Loop through recipe index
for i in range(1,13):
    num = '0'+str(i)
    print(num)
    try:
        site = requests.get(bbj+num, headers=headers)
    except requests.exceptions.ConnectionError:
        pass
    print('hello webpage is')
    print site.status_code
    print site.raw

    #soup = BeautifulSoup(webpage.content).find_all('li')
    webpage = site.content
    soup = BeautifulSoup(webpage.decode('utf-8'), "lxml").find_all("h3", class_ = "teaser-item__title") 


    # Find all meals/bars
    for elem in soup:
        meal = elem.get_text()
        link = elem.a["href"]
        meal_pages[meal]=link
        
# Loop through rest of the recipes
for i in range(14,num_max):
    num = str(i)
    print(num)
    try:
        site = requests.get(bbj+num, headers=headers)
    except requests.exceptions.ConnectionError:
        pass
    print('hello webpage is')
    print site.status_code
    print site.raw

    #soup = BeautifulSoup(webpage.content).find_all('li')
    webpage = site.content
    soup = BeautifulSoup(webpage.decode('utf-8'), "lxml").find_all("h3", class_ = "teaser-item__title") 


    # Find all meals/bars
    for elem in soup:
        meal = elem.get_text()
        link = elem.a["href"]
        meal_pages[meal]=link


count = 0

# Store all information in a csv file    
with open("meals_page.csv", "w") as toWrite:
    writer = csv.writer(toWrite, delimiter=",")
    writer.writerow(["meal name", "page link"])
    for meal in meal_pages.keys():
        name = meal
        link = meal_pages[meal]
        print("name is ", name)
        print("link is ", link)
        
        # Check for asscii characters
        if(prep.is_ascii(name) == False):
                print (" asscii error on  ", name)
                #name= prep.to_unicode(name)
                print (" changed to  ", name)
            
        elif(prep.is_ascii(link) == False):
                print (" asscii error on  ", link)
                #link= prep.to_unicode(link)
                print (" changed to  ", link)
        else:
            writer.writerow([name, link])
            count = count + 1
print count