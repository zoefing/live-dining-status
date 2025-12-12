# import statements

# import data from python file that scrapes smith dining website
# import relevant flask elements
from flask import Flask, redirect, render_template, request, session, url_for

import scraper
import os

# create flask app
app = Flask(__name__)

# time of day
from datetime import datetime
import pytz

# initialize session
app.secret_key = os.environ.get("SECRET_KEY", "your_secret_key_here")

# get meal options from scraper
meal_options = scraper.meal_options


# setup app
@app.route("/")
def index():
    # # debugging
    # print("available dining halls from scraper:")

    # iterate through each key (dining hall)
    for key in meal_options.keys():
        print(f"  - {key}")

    # create dropdown using dining hall name keys
    options = list(meal_options.keys())
    print(options)

    # render template (i.e., boot up main index.html page with the variables fed in)
    return render_template("index.html", options=options)


# get user input from dropdown
@app.route("/handle_selection", methods=["POST"])
def handle_selection():
    # get the selected value from the dropdown data
    if request.method == "POST":
        # acquire selection
        selected_option = request.form.get("dropdown_select")

        # storing dining hall name
        # this is just cosmetic, no value to program

        # initialize variable name
        session["dining_hall_name"] = selected_option

        # deal with differing dining hall format types
        if selected_option == "chase_duckett":
            selected_option = "Chase/Duckett"
            session["dining_hall_name"] = selected_option
        elif selected_option == "cutter_ziskind":
            session["dining_hall_name"] = selected_option
            selected_option = "Cutter/Ziskind"
        elif selected_option == "ziskind_kosher":
            selected_option = "Ziskind Kosher"
            session["dining_hall_name"] = selected_option
        elif selected_option == "king_scales":
            selected_option = "King Scales"
            session["dining_hall_name"] = selected_option
        elif selected_option == "northrop_gillett":
            selected_option = "Northrop Gillett"
            session["dining_hall_name"] = selected_option
        else:
            selected_option = (str(selected_option)).capitalize()
            session["dining_hall_name"] = selected_option

        # reformat selection name to work with url nav (i.e., remove whitespace and slashes)
        menu = (str(selected_option)).replace(" ", "_").replace("/", "_").lower()

        # # debugging
        # print(f"Selected option: {selected_option}")
        # print(f"Converted menu key: {menu}")

        # check if the menu exists before proceeding
        if menu in meal_options:
            # # debugging
            # print(f"menu items = {meal_options[menu]}\n")

            # store menu items in session
            session["menu_items"] = meal_options[menu]

            # redirect to the new page with the variable in the URL
            return redirect(url_for("dining", variable=menu))

        # error for if menu not found
        else:
            # throw error and clarifiying response
            print(f"ERROR: Menu key '{menu}' not found in meal_options")
            print(f"Available keys: {list(meal_options.keys())}")

            # redirect back to home
            return redirect(url_for("index"))

    # return
    return redirect(url_for("index"))


# display data on
@app.route("/dining/<variable>")
def dining(variable):
    # get current time for this request
    now = datetime.now()
    
    # get menu items from session
    menu_items = session.get("menu_items", {})
    print(f"menu items: {menu_items}")

    # get meal time by time of day
    # set current time
    meal_time = ""
    print(f"hour: {now.hour}")

    # 7 AM to 12 PM - breakfast
    if 7 <= now.hour < 12:
        meal_time = "breakfast"
    # 12 PM to 5 PM - lunch
    elif 12 <= now.hour < 17:
        meal_time = "lunch"
    # 5 PM to 8 PM - dinner
    elif 17 <= now.hour < 20:
        meal_time = "dinner"
    # outside meal hours - default to next meal
    else:
        if now.hour < 7:
            meal_time = "breakfast"
        else:
            meal_time = "dinner"

    # if (now.hour == 7 and now.minute >= 00) or (11 <= now.hour < 29):
    #     meal_time = "breakfast"

    # elif (now.hour == 11 and now.minute >= 30) or (12 <= now.hour < 13) or (now.hour == 4 and now.minute < 29):
    #     meal_time = "lunch"

    # elif (now.hour == 16 and now.minute >= 30) or (17 <= now.hour < 20):
    #     meal_time = "dinner"

    print(f"time: {meal_time}")

    timed_menu_items = []
    meal_available = True

    if meal_time == "breakfast":
        timed_menu_items = menu_items.get("breakfast", [])
        if not timed_menu_items:
            meal_available = False

    elif meal_time == "lunch":
        timed_menu_items = menu_items.get("lunch", [])
        if not timed_menu_items:
            meal_available = False

    elif meal_time == "dinner":
        timed_menu_items = menu_items.get("dinner", [])
        if not timed_menu_items:
            meal_available = False

    # get stashed dining hall name
    dining_hall_name = session.get("dining_hall_name")

    # debugging
    print(f"timed menu items: {timed_menu_items}")

    # render the new page template with the passed variable
    return render_template(
        "dining.html",
        variable=variable,
        items=timed_menu_items,
        dining_hall=dining_hall_name,
        meal_type=meal_time,
        meal_available=meal_available,
    )


# run program
if __name__ == "__main__":
    app.run(debug=True)