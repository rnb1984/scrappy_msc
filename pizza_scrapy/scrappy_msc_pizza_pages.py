from bs4 import BeautifulSoup
import json
import requests
import os, csv
import scrape_uni_writer as prep

headers = {'User-agent': 'Mozilla/5.0'}
beebgf = 'http://www.bbcgoodfood.com/search/recipes?query=#page='
# note for page=14 plus works but below has to be page=09, page=012
# range page= to page=647
bbj = 'http://www.bbcgoodfood.com/search/recipes?query=pizza#query=pizza&page='
num_max = 7
beeb_end= '&path=kcal/%5B41+TO+658%5D'

pizza_check = { "bread", "breads", "naan", "naans", "nan", "flatbread", "flatbreads", "pitta", "pies", "pie", "roll", "rolls", "calzone", "calzones", "puff", "puffs", "baguette", "baguettes", "toasties", "toast", "pizzaiola", "s'mores", "pizzadillas", "stromboli", "tart","tarts", "focaccia" }
pizza_pages = {}

# check link is a pizza
def is_pizza(title):
    pos_pizza = title.split()
    for pizza in pos_pizza:
        pizza = pizza.lower()
        for not_pizza in pizza_check:
            if (pizza == not_pizza):
                return False
    return True

all_sites = []
down_i = num_max
for i in range(0,num_max):
    print i
    num = str(i)
    try:
            #site = requests.get(bbj+num+beeb_end, headers=headers)
            site = requests.get("http://www.bbcgoodfood.com/search/recipes/kcal/[41%20TO%20658]?query=pizza&page="+num, headers=headers)
            webpage = site.content
            soup = BeautifulSoup(webpage.decode('utf-8'), "lxml").find_all("h3", class_ = "teaser-item__title")
            all_sites.append(soup)
            
    except requests.exceptions.ConnectionError:
        pass



# Loop through recipe index
for i in range(0,len(all_sites)):
    # could use num = '0' +str(i)
    #num = str(i)
    #print(num)
    print i
    
    #try:
        #site = requests.get(bbj+num+beeb_end, headers=headers)
        #site = requests.get(all_sites[i], headers=headers)
    #except requests.exceptions.ConnectionError:
        #pass
    #print('hello webpage is')
    #print site.status_code
    #print site.raw

    #webpage = site.content
    #soup = BeautifulSoup(webpage.decode('utf-8'), "lxml").find_all("h3", class_ = "teaser-item__title") 

    
    # Find all pizza
    for elem in all_sites[i]:
        print('got here too')
        pizza = elem.get_text()
        print pizza
        is_this_pizza = is_pizza(pizza)
        if (is_this_pizza):
            link = elem.a["href"]
            pizza_pages[pizza]=link

count = 0


# Store all information in a csv file    
with open("pizzas_page_all.csv", "w") as toWrite:
    writer = csv.writer(toWrite, delimiter=",")
    writer.writerow(["pizza name", "page link"])
    for pizza in pizza_pages.keys():
        name = pizza
        link = pizza_pages[pizza]
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