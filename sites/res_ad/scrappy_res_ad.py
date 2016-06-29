from bs4 import BeautifulSoup
import requests
import os, csv
import scrape_res_writer as prep


# Set headers and open up url 
headers = {'User-agent': 'Mozilla/5.0'}
rez = 'https://www.residentadvisor.net/clubs.aspx?ai=340'
webpage = requests.get(rez, headers=headers)
webpage = webpage.content
soup = BeautifulSoup(webpage.decode('utf-8'), "lxml").find_all("li", class_ = "clearfix")

clubs = {}
club_sites={}
club_own_sites={}

# Find all Clubs/bars
for elem in soup:
    address = elem.find(class_="fl grey mobile-off").get_text()
    club = elem.find(class_="fl").get_text()
    clubs[club] = address
    link = elem.a["href"]
    club_sites[club]=link

# Find all Clubs/bars offical site
for site in club_sites:
    url = 'https://www.residentadvisor.net' + club_sites[site]
    webpage = requests.get(url, headers=headers)
    webpage = webpage.content
    soup = BeautifulSoup(webpage, "lxml")
    soup = soup.find_all('a')
    for link in soup:
        if (link.get_text() =='Website'):
            club_own_sites[site]=link['href']
    # Find Events
    # if the page has li, attribute = itemscope, class="standard"
    # get img src
    # get date in class="bbox", h1.get_text()
    # get event name in h1, itemprop="summary", class="title" .get text()
    # get dj's in span, class="grey" .get text()
    
    # Find all clubs for year (even past events)
    # url = url + &show=events
    url = url + '&show=events'
    
    # tag = article
    # h1 .get_text() name of event
    # p class="date" .get text()
    # pop ularity of event p class="counter" , span .get_text() is how popular
    # a ['href'] of event page
    # img ['src'] should be image 

# Store all information in a csv file    
with open("clubs.csv", "w") as toWrite:
    writer = csv.writer(toWrite, delimiter=",")
    writer.writerow(["club", "address", "link", "site"])
    for clubInfo in clubs.keys():
        name = clubInfo
        address = clubs[clubInfo]
        link = club_sites[clubInfo]
        site = 'None'
        for bar in club_own_sites:
            if (clubInfo == bar):
                site = club_own_sites[clubInfo]
                
        
        # Check for asscii characters
        if(prep.is_ascii(address) == False):
                print (" asscii error on  ", address)
                address= prep.to_unicode(address)
                print (" changed to  ", address)
        elif(prep.is_ascii(name) == False):
                print (" asscii error on  ", name)
                name= prep.to_unicode(name)
                print (" changed to  ", name)
            
        elif(prep.is_ascii(link) == False):
                print (" asscii error on  ", name)
                name= prep.to_unicode(name)
                print (" changed to  ", name)
        else:
            writer.writerow([name, address, link, site])
