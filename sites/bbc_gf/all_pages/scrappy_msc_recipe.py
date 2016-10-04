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

meal_ingr={}
meal_mth={}
meal_nuit={}
meal_pages={}
meals=[]

# Load site information
with open('meals_pages.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        meals.append(row['meal name'])
        meal_pages[row['meal name']] = row['page link']
        
    
#print meal_pages
count=0
max_meal = 100
# Loop through recipe index
for i in range(0,max_meal):
    count = count + 1
    
    dish_name = meals[i]
    beeb_end = meal_pages[dish_name]
    print( beebgf + beeb_end )
    
    try:
        site = requests.get( beebgf + beeb_end, headers=headers )
    except requests.exceptions.ConnectionError:
        pass
    
    print('hello webpage is')
    print site.status_code
    print site.raw
    print count

    webpage = site.content
    soup = BeautifulSoup( webpage.decode('utf-8'), "lxml")
    soup_ingr = soup.find_all( "li", class_ = "ingredients-list__item")
    ingrd=[]
    
    j = 1
    # Find all meals/bars
    for elem in soup_ingr:
        # checkschildren aren't in tool tip
        for child in elem.children:
            if hasattr(child, "gf-tooltip"):
                pass
            else:
                if hasattr(child, 'get_text'):
                    ingrd.append(child.get_text())
                else:
                    #print child
                    ingrd.append(child)
    
    # get all the methods
    soup_mth = soup.find_all( "li", class_ = "method__item")
    methods = []
    for elem in soup_mth:
        methods.append(elem.p.get_text())
    
    meal_ingr[dish_name]= ingrd
    meal_mth[dish_name]= methods
    
    # find parent of span "nutrition__label nutrition__label--low" ||  "nutrition__label"
    # get text from li
    soup_n_label = soup.find_all("span", class_ = "nutrition__label")
    soup_n_val = soup.find_all("span", class_ = "nutrition__value")

    # Find nutritional information
    #for elem in soup:
    #    meal_nuit = { dish_name : { soup_n_label[elem] : soup_n_val [elem] } }


count = 0

# Store all information in a csv file    
with open("meals_recipe.csv", "w") as toWrite:
    writer = csv.writer(toWrite, delimiter=",")
    writer.writerow(["meal name", "ingredients", "method"])
    
    #for meal in meal_pages.keys():
    for i in range(0,max_meal):
    
        meal = meals[i]
        name = meal
        ingredients = meal_ingr[meal]
        method = meal_mth[meal]
        print("name is ", name)
        print("method is ", method)
        
        writer.writerow([name, ingredients, method])
        count = count + 1
print count