from bs4 import BeautifulSoup
import json
import requests
import os, csv
import scrape_uni_writer as prep

headers = {'User-agent': 'Mozilla/5.0'}
beebgf = 'http://www.bbcgoodfood.com'
num_max = 9167
beeb_end = ''
dish_name = ''

meals = {}
meal_pages={}
meal_ingr={}
meal_mth={}
meal_nuit={}

# Got to site

# Loop through recipe index
for i in range(1,num_max):
    
    beebgf = ''
    print( beebgf )
    
    try:
        site = requests.get( beebgf + beeb_end, headers=headers )
    except requests.exceptions.ConnectionError:
        pass
    
    print('hello webpage is')
    print site.status_code
    print site.raw

    #soup = BeautifulSoup(webpage.content).find_all('li')
    webpage = site.content
    soup = BeautifulSoup( webpage.decode('utf-8'), "lxml")
    soup_ingr = soup.find_all( "li", class_ = "ingredients-list__item")
    soup_mth = soup.find_all( "li", class_ = "method__item")
    
    # find parent of span "nutrition__label nutrition__label--low" ||  "nutrition__label"
    # get text from li
    soup_n_label = soup.find_all("span", class_ = "nutrition__label")
    soup_n_val = soup.find_all("span", class_ = "nutrition__value")
    
    meal_ingr={dish_name : soup_ingr }
    meal_mth={dish_name : soup_mth }
    

    # Find nutritional information
    for elem in soup:
        meal_nuit = { dish_name : { soup_n_label[elem] : soup_n_val [elem] } }


count = 0

# Store all information in a csv file    
with open("meals_recipe.csv", "w") as toWrite:
    writer = csv.writer(toWrite, delimiter=",")
    writer.writerow(["meal name", "ingredients", "method"])
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