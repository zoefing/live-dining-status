# getting live data
import requests
from bs4 import BeautifulSoup

# regex
import re

# get live info from smith dining webpage
url = "https://www.smith.edu/diningservices/menu_poc/cbord_menus.php/robots.txt" 

# initialize meal_options dictionary to store all dining hall data
meal_options = {}

# fetch website content using requests
try:
    # get content
    response = requests.get(url)
    # check if the request was successful
    response.raise_for_status()
    # save cotent
    html_content = response.content
    
# throw exception if not working
except requests.exceptions.RequestException as e:
    print(f"Error fetching the URL: {e}")
    exit()

# create a beautifulsoup object to parse the HTML
soup = BeautifulSoup(html_content, "html.parser")

# find elements by their tag name ('div') and class name
target_class = "smith-menu-wrapper context"
div_elements = soup.find_all("div", class_=target_class)

# iterate through the found elements and extract data (e.g., text)
if div_elements:
    # # debugging
    # print(f"Found {len(div_elements)} div(s) with class '{target_class}':")
    for index, div in enumerate(div_elements):
        # # debugging
        # print(f"--- Element {index + 1} ---")
        # get the text content of the div
        contents = div.get_text(strip=True)
        # # debugging
        # print(f"contents: {contents}\n")

        # split contents by regex (two words next to eachother = new line)
        regex_split = regex_split = re.split(r'(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])', contents)
        
        # # debugging
        # print(f"regex split: {regex_split}\n")

        # initialize data
        dining_hall = regex_split[0]
        breakfast = []
        lunch = []
        dinner = []

        # get indices for each meal
        if "BREAKFAST" in regex_split:
            breakfast_index = regex_split.index("BREAKFAST")
            if "LUNCH" in regex_split:
                lunch_index = regex_split.index("LUNCH")
                breakfast = regex_split[breakfast_index + 1 : lunch_index]
                if "DINNER" in regex_split:
                    dinner_index = regex_split.index("DINNER")
                    lunch = regex_split[lunch_index + 1 : dinner_index]
                    dinner = regex_split[dinner_index + 1 :]
                else:
                    lunch = regex_split[lunch_index + 1 :]
            else:
                breakfast = regex_split[breakfast_index + 1 :]
        else:
            if "DINNER" in regex_split:
                dinner_index = regex_split.index("DINNER")
                dinner = regex_split[dinner_index + 1 :]

        # # debugging
        # print(f"dining hall: {dining_hall}\n")
        # print(f"breakfast: {breakfast}\n")
        # print(f"lunch: {lunch}\n")
        # print(f"dinner: {dinner}\n")

        # store data in structured format
        dining_hall_key = dining_hall.replace(" ", "_").replace("/", "_").lower()
        
        # # debugging
        # print(dining_hall_key)

        # make sure dining hall key is valid
        # # if not
        if dining_hall_key not in meal_options:
            # initialize
            meal_options[dining_hall_key] = {}
        
        # if breakfast time
        if breakfast:
            # load breakfast options
            meal_options[dining_hall_key]["breakfast"] = breakfast
            # # debugging
            # print(f"breakfast for {dining_hall}: {breakfast}\n")

        # if lunch time
        if lunch:
            # load lunch options
            meal_options[dining_hall_key]["lunch"] = lunch
            # # debugging
            # print(f"lunch for {dining_hall}: {lunch}\n")

        # if dinner time
        if dinner:
            # load dinner options
            meal_options[dining_hall_key]["dinner"] = dinner
            # # debugging
            # print(f"dinner for {dining_hall}: {dinner}\n")

# # debugging
# else:
#     # print(f"No div elements found with class '{target_class}'.")
   
# # debugging 
# print(f"\nfinal meal_options structure: {meal_options}")