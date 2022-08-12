import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

names = []
images = []
ratings = []
details_arr = []

def scrapUrl(url):
    req = requests.get(url)
    content = BeautifulSoup(req.content, 'html.parser')
    maindivs = content.find("div", {"class": "_1YokD2 _3Mn1Gg"})
    targetdivs = maindivs.find_all("div", {"class": "_1AtVbE col-12-12"})

    for each in targetdivs:
        name =  each.find("div", {"class": "_4rR01T"})
        image =  each.find("img", {"class": "_396cs4 _3exPp9"})
        rating =  each.find("div", {"class": "_3LWZlK"})
        details =  each.find_all("li", {"class": "rgWa7D"})

        if name != None:
            filter_name = str(name.string)
            names.append(filter_name)
        
        if image != None:
            filter_image = image['src']
            images.append(filter_image)
        
        if rating != None:
            filter_rating = str(rating)
            result = re.search('>(.*)<img', filter_rating)
            ratings.append(result.group(1))

        if len(details) > 0:
            dt = ""
            for each in details:
                dt += str(each.string)
            details_arr.append(dt)

    if(len(names)==len(images)==len(ratings)==len(details_arr)):
        df = pd.DataFrame({'name': names, 'image': images, 'rating': ratings, 'detail':details_arr})
        df.to_csv('output.csv', mode='a', index=False, header= True)
        print("Data scrap successfully. CSV file generated")


scrapUrl('https://www.flipkart.com/mobiles/mi~brand/pr?sid=tyy%2C4io&otracker=nmenu_sub_Electronics_0_Mi&page=2')