from bs4 import BeautifulSoup
import json
import requests
import os, csv
import scrape_uni_writer as prep

headers = {'User-agent': 'Mozilla/5.0'}


# DO THIS FISRT !!
# METHOD map to exsisting methods
list_of_techniques = 'https://en.wikipedia.org/wiki/List_of_cooking_techniques'

try:
        site_one = requests.get( list_of_techniques, headers=headers )
except requests.exceptions.ConnectionError:
        pass
    
wikipage = site_one.content
soup = BeautifulSoup( wikipage.decode('utf-8'), "lxml")
soup_meth = soup.find_all("li") # find first a of children

method_list = []
# if get text < 1 
# if the text of the a has a string more than three don't store it

methods_correct = True
for elem in soup_meth:
    all_elem = elem.find('a')
    if (hasattr(all_elem,'string')):
        for child in all_elem:
            if(hasattr(child,'string')):
                method = child.string
                print method
                
                if(hasattr(method,'split()')!=False):
                    method_string = method.split()
                    letters = list(method)
                    print ("got here")
                    if len(list(letters)) > 1 :
                        if len(method_string) <= 3:
                            method_list.append(method)
                            
print("----------------------------- Out!!")
count=0

# Store all information in a csv file    
with open("cooking_methods.csv", "w") as toWrite:
    writer = csv.writer(toWrite, delimiter=",")
    writer.writerow(["method"])
    
    
    #for meal in meal_pages.keys():
    for method in method_list:
        if(prep.is_ascii(method) == False):
                print (" asscii error on  ", method)
        else:
            method = method.decode('utf-8')
            writer.writerow([method])
            count = count + 1
print count