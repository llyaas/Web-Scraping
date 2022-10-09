
# bs4 (BeautifulSoup) is a python module, which is famously used for parsing text as HTML and then performing actions in it, such as
# finding specific HTML tags with a particular class/id, or listing out all the li tags inside the ul tags.
# Selenium, on the other hand, is used to interact with the webpage.
# It is famously used for automation testing, such as testing the functionality of a website (Login/Logout/etc.)
# but can be also used to interact with the page such as clicking a button, etc.
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests
import csv


# NASA Expoplanet URL
START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"

# creating webdriver object & initialising it
browser = webdriver.Chrome(
    "C:/Users/adil_/Documents/CodingClasses/C127/chromedriver")
browser.get(START_URL)

time.sleep(10)

# Defining a function called scrape which will contain list called headers & planet_data

# Enumerate is a function that returns the index along with the element.
# Enumerate will give us both the index and the element on that index, instead of just the index that a traditional loop gives.
# As we get the index (number of the element ) Using this index, if the index is 0 ( first element),
# Every element here contains the <a> tag or the anchor tag so we are first finding the anchor tag inside the li_tag(list item),
# and then copying the inner HTML of it.
# Else, we want to directly copy the inner HTML of the li_tag.
# To facilitate this, in case a column is empty and we get an error, we are going to use the try except block.
# Lastly, we will append this temp_list into the planet_data.



planets_data = []
#add the new headers, that is, the new data that is available on the new page 
headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date", "hyperlink", 
            "planet_type", "planet_radius", "orbital_radius", "orbital_period", "eccentricity"]

def scrape():
     
    for i in range(1, 5):
        while True:
            time.sleep(2)

            soup = BeautifulSoup(browser.page_source, "html.parser")

            # Check page number
            # create a new function that will take these hyperlinks one by one, get the HTML and then we will scrape the data.
            # To make sure that we are scraping pages one by one, we’ll add a code in the scrape() function to check the current page number

            current_page_num = int(soup.find_all(
                "input", attrs={"class", "page_num"})[0].get("value"))

            if current_page_num < i:
                browser.find_element(
                    By.XPATH, value = '//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            elif current_page_num > i:
                browser.find_element(
                    By.XPATH, value = '//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
            else:
                break

        # running a for loop to travel over all the ul tags
        for each_ul_tag in soup.find_all("ul", attrs = {"class", "exoplanet"}):
            li_tags=each_ul_tag.find_all("li")
            temp_list=[]
            # running a for loop to travel over each li tag inside each ul tag
            for index, each_li_tag in enumerate(li_tags):
                if index == 0:
                    # because the first li tag that means index = 0 has another tag inside it
                    # the li tag at index 0 contains anchor tag<a>...</a>
                    # for this we need to make sure that we treat the first li tag differently than others
                    temp_list.append(each_li_tag.find_all("a")[0].contents[0])
                else:  # this one is for all the plain li tags
                    try:
                        temp_list.append(each_li_tag.contents[0])
                    except:
                        temp_list.append("")

            # acessing the data of the first li tag
            # the li tag contains a single anchor tag which has href attribute
            # we need to store the value of hyperlinks for each of these li tags & append it to the final data list
            hyperlink_li_tag=li_tags[0]

            temp_list.append("https://expoplanets.nasa.gov" +
                             hyperlink_li_tag.find_all("a", href=True)[0]["href"])

            planets_data.append(temp_list)

        # we want to go to the next stage after our code is done with all the ul tags <ul>...</ul> of the current page
        # we can go to the next page with the folowing code
        # we find an element with xpath
        # xpath can be used to navigate through different elements & attributes in an XML document
        # xpath is a syntax for defining parts of an XML document
        browser.find_element(
            "xpath", '//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()



# calling the function scrape
scrape()

# now earlier, we created a soup
# object where we passed the
# browser’s page source and parsed it
# as html. This time, since we are not
# going to use selenium, We can get the page’s
# HTML by making a GET
# request.For that, we will import
# requests module

new_planets_data = []

def scrape_more_data(hyperlink):
    try:
#         Here, we are first getting the page,
# and then we are parsing the contents of the page as HTML.
        page = requests.get(hyperlink)
      
        soup = BeautifulSoup(page.content, "html.parser")

# create a new list
# new_planets_data to save data from these new pages, and ask them to scrape the data like before.
        temp_list = []
        for tr_tag in soup.find_all("tr", attrs={"class": "fact_row"}):
            td_tags = tr_tag.find_all("td")
          
            for td_tag in td_tags:
                try: 
                    temp_list.append(td_tag.find_all("div", attrs={"class": "value"})[0].contents[0])
                except:
                    temp_list.append("")
                    
        new_planets_data.append(temp_list)

    except:
        time.sleep(1)
        scrape_more_data(hyperlink)

#Calling method and check the list new_planets_data.
for index, data in enumerate(planets_data):
    scrape_more_data(data[5])
    print(f"scraping at hyperlink {index+1} is completed.")

print(new_planets_data[0:10])


# Now we have 2 lists,planets_data and new_planets_data.
# In new_planets_data, a special
# character ‘\n’ is present. we need to
# remove it before saving it to csv file.
# Also, we want to merge the two lists.
# Adding 2 lists creates 1 final list with
# elements from both the lists in the
# same order.
final_planet_data = []

for index, data in enumerate(planets_data):
    new_planet_data_element = new_planets_data[index]
    new_planet_data_element = [elem.replace("\n", "") for elem in new_planet_data_element]
    new_planet_data_element = new_planet_data_element[:7]
    final_planet_data.append(data + new_planet_data_element)





with open("planetdata_203_hyperlinks.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(planets_data)