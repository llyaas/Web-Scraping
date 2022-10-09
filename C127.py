from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"
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


def scrape():
    headers = ["name", "light_years_from_earth",
               "planet_mass", "stellar_magnitude", "discovery_date"]
    planet_data = []
    for i in range(0, 203):
        soup = BeautifulSoup(browser.page_source, "html.parser")
        # running a for loop to travel over all the ul tags
        for each_ul_tag in soup.find_all("ul", attrs={"class", "exoplanet"}):
            li_tags = each_ul_tag.find_all("li")
            temp_list = []
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
            planet_data.append(temp_list)
        # we want to go to the next stage after our code is done with all the ul tags <ul>...</ul> of the current page
        # we can go to the next page with the folowing code
        # we find an element with xpath
        # xpath can be used to navigate through different elements & attributes in an XML document
        # xpath is a syntax for defining parts of an XML document
        browser.find_element(
            "xpath", '//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()

    with open("planetdata_203.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(planet_data)


# calling the function scrape
scrape()
# bs4 (BeautifulSoup) is a python module, which is famously used for parsing text as HTML and then performing actions in it, such as
# finding specific HTML tags with a particular class/id, or listing out all the li tags inside the ul tags.
# Selenium, on the other hand, is used to interact with the webpage.
# It is famously used for automation testing, such as testing the functionality of a website (Login/Logout/etc.)
# but can be also used to interact with the page such as clicking a button, etc.
