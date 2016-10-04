from bs4 import BeautifulSoup
import json
import requests
import re
import os, csv
import scrape_uni_writer as prep

# ingredients list from bbc food
ingredients =[]
with open('ingredients_simple.csv', 'rb') as csvfile:
    ingr_file = csv.reader(csvfile, delimiter=' ')
    for ingr in ingr_file:
        ingredients.append(' '.join(ingr))
not_ingr=[]

# check if it has ingredients from the list if not then store in non igr
def find_ingredient(poss_ingr):

    sentance  = poss_ingr.split()
    for poss in sentance:
        
        for ingr in ingredients:
            plural = ingr.lower() +'s'
            
            if (ingr.lower() == poss.lower()):
                return ingr
                
            if (plural == poss.lower()):
                return plural
    not_ingr.append(poss_ingr)
    return "x"

# print out non ingreidients


headers = {'User-agent': 'Mozilla/5.0'}
beebgf = 'http://www.bbcgoodfood.com'
beeb_end = ''
dish_name = ''

pizza_base= {}
# BASE to check INGREDIENTS


meal_ingr={}
meal_mth={}
meal_nuit={}
pizza_pages={}
meals=[]

# Load site information
print('lets go')
with open('pizzas_page.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        meals.append(row['pizza name'])
        pizza_pages[row['pizza name']] = row['page link']
        

count=0
max_meal = 8

# Loop through recipe index
for i in range(0,max_meal):
    count = count + 1
    
    dish_name = meals[i]
    beeb_end = pizza_pages[dish_name]
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
    # Find all ingredients
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
                    chil_split = re.split(r"[,; ]+", child)
                    for word in chil_split:
                        food = find_ingredient(word)
                        if (food != 'x'):
                            ingrd.append(food)
    
    soup_list_ingr = soup.find_all( "a",class_="ingredients-list__glossary-link")
    
    # check the links for the ingredients glossary
    for elem in soup_list_ingr:
        ingrd.append(elem.get_text()) 
        
        
    
    
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
with open("pizza_recipe.csv", "w") as toWrite:
    writer = csv.writer(toWrite, delimiter=",")
    writer.writerow(["meal name", "ingredients", "method"])
    
    #for meal in meal_pages.keys():
    for i in range(0,max_meal):
    
        meal = meals[i]
        name = meal
        ingredients = meal_ingr[meal]
        method = meal_mth[meal]
        print("name is ", name)
        print("ingredients is ", ingredients)
       # print("method is ", method)
        
        writer.writerow([name, ingredients, method])
        count = count + 1
print count