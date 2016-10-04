from string import ascii_lowercase
from bs4 import BeautifulSoup
import json
import requests
import os, csv
import scrape_uni_writer as prep

headers = {'User-agent': 'Mozilla/5.0'}
url = 'http://www.bbc.co.uk/food/ingredients/by/letter/'

ingredients= []

for letter in ascii_lowercase:
    new_url= url + letter
    print letter
    
    try:
        site = requests.get(new_url, headers=headers)
    except requests.exceptions.ConnectionError:
        pass
    
    print site.status_code
    print site.raw
    
    webpage = site.content
    
    soup = BeautifulSoup(webpage.decode('utf-8'), "lxml").find_all("li", class_ = "resource food") 
 
    for item in soup:
        ingr = item.text.strip().split('\n')
        print 'soup test'
        print ingr
        
        if ingr[0].startswith( 'Related' ) == False:
            ingredients.append(ingr[0])

count = 0


# Store all information in a csv file    
with open("ingredients_simple.csv", "w") as toWrite:
    
    writer = csv.writer(toWrite, delimiter=",")
    writer.writerow(["ingredient name"])
    
    for ingredient in ingredients:
        name = ingredient.encode('utf-8').strip()
        print("name is ", name)

        writer.writerow([name])
        count = count + 1
print count