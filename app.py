# import statements

# import data from python file that scrapes smith dining website
import scraper

# import relevant flask elements
from flask import Flask, redirect, render_template, request, session, url_for

# create flask app
app = Flask(__name__)

# initialize session
app.secret_key = "your_secret_key_here" 

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
            return redirect(
                url_for("dining", variable=menu, stash=selected_option)
            )
            
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
    # get menu items from session
    menu_items = session.get("menu_items", {})
    # get stashed dining hall name
    dining_hall_name = session.get("dining_hall_name")
    # render the new page template with the passed variable
    return render_template("dining.html", variable=variable, menu_items=menu_items, dining_hall=dining_hall_name)

# run program
if __name__ == "__main__":
    app.run(debug=True)