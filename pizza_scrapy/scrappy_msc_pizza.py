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
pizza_pages={}
images={}
urls = {}
meals=[]

# Load site information
with open('pizzas_page_all.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    i = 0
    for row in reader:
        meals.append(row['pizza name'])
        meals[i] = meals[i].strip()
        pizza_pages[meals[i]] = row['page link']
        i = i + 1
        

count=0
max_meal = len(meals)

# Loop through recipe index
for i in range(0,max_meal):
    count = count + 1
    
    # find and store recipe urls
    dish_name = meals[i]
    beeb_end = pizza_pages[dish_name]
    print( beebgf + beeb_end )
    urls[dish_name] = beeb_end

    
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
    
    # soup for image urls
    soup_images = soup.find("img", itemprop="image")
    images[dish_name] = soup_images["src"]
    print images[dish_name]
    
    # soup for ingredients
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
        
    print dish_name
    meal_ingr[dish_name]= ingrd
    



count = 0

# Store all information in a csv file    
with open("pizza_recipe.csv", "w") as toWrite:
    writer = csv.writer(toWrite, delimiter=",")
    writer.writerow(["meal name", "image_url", "ingredients", "recipe_urls"])
    
    #for meal in meal_pages.keys():
    for i in range(0,len(meals)):
        
        meal = meals[i]
        name = meal
        ingredients = meal_ingr[meal]
        image_url = images[meal]
        url = urls[meal]
        
        #print("name is ", name)
        #print("ingredients is ", ingredients)

        writer.writerow([name,image_url, ingredients, url])
        count = count + 1
print count


# list all the toppings used
all_toppings = {}

for pizza in meal_ingr:
    for i in meal_ingr[pizza]:
        if i in all_toppings:
            all_toppings[i] = all_toppings[i] + 1
        else:
            all_toppings[i] = 1

print all_toppings

with open("pizza_toppings.csv", "w") as toWrite:
    writer = csv.writer(toWrite, delimiter=",")
    writer.writerow([ "ingredient", "number"])
    
     #for meal in meal_pages.keys():
    for ing in all_toppings:
        
        num = all_toppings[ing]
        ingredient = ing

        writer.writerow([ingredient, num])