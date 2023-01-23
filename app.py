# Import OS module
import os

# Import required dependancies from the associated libraries
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required

# Configure application for flask to run app.py
app = Flask(__name__)


# Configure CS50 Library to use SQLite database cookbook
db = SQL("sqlite:///cookbook.db")


# Configure session to use filesystem (instead of signed cookies) borrowed from PSET 9 finance
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Borrowed from PSET9 finance. After each route request it will ensure the responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Index or homepage for the application. Simply takes the user to the index.html template
@app.route("/")
def index():
    return render_template("index.html")


# Login route. Allows the user to login via POST or visit the login page via GET. Login will check the users details are in the database and create a session for the associated user id.
@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget previous session
    session.clear()

    # User accessed via POST so perofrm log in steps and checks from the user database
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Please enter a username")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Please enter a password")
            return render_template("login.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("Username or password is incorrect")
            return render_template("login.html")

        # Remember which user has logged in using the session feature
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User accessed via GET so render the login template
    else:
        return render_template("login.html")


# Login route. Allows the user to logout of clear the current session
@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


# Register route. Allows the user to register for the web app and save their details into the users table in the cookbook database
@app.route("/register", methods=["GET", "POST"])
def register():

    # User accessed via POST so perform registration steps and checks before adding user to database
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Please enter a username")
            return redirect("/register")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Please enter a passowrd")
            return redirect("/register")

        # Ensure password was confirmed
        elif not request.form.get("confirmation"):
            flash("Pease confirm password")
            return redirect("/register")

        # Ensure password matches with confirmed password
        elif request.form.get("password") != request.form.get("confirmation"):
            flash("Passwords do not match")
            return redirect("/register")

        # Query database for username
        user = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # If username already found and rows is returned 1 username already exists
        if len(user) == 1:
            flash("Username already taken")
            return redirect("/register")

        # Create variables from user input
        username = request.form.get("username")
        hash = generate_password_hash(request.form.get("password"))

        # Insert the new user into the database
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)

        # Take the user back to the login page to login with new credentials and flash success message
        flash('Success!')
        return redirect("/login")

    # User accessed via GET so render the registration template
    else:
        return render_template("register.html")


# Password route. Allows the user to change their current password in the database
@app.route("/password", methods=["GET", "POST"])
@login_required
def password():

    # User accessed via POST so perform checks and password change steps
    if request.method == "POST":

        # Ensure new password was submitted
        if not request.form.get("new password"):
            flash("Please enter new password")
            return redirect("/password")

        # Ensure old password was submitted
        elif not request.form.get("old password"):
            flash("Please enter old password")
            return redirect("/password")

        # Ensure password was confirmed
        elif not request.form.get("confirm"):
            flash("Please confirm new password")
            return redirect("/password")

        # Ensure password matches with confirmed password
        elif request.form.get("new password") != request.form.get("confirm"):
            flash("Passwords do not match")
            return redirect("/password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

        new_hash = generate_password_hash(request.form.get("new password"))

        # Ensure old password is correct
        if not check_password_hash(rows[0]["hash"], request.form.get("old password")):
            flash("Password is incorrect")
            return redirect("/password")

        # Update the users password in the database
        else:
            db.execute("UPDATE users SET hash = ? WHERE id = ?", new_hash, session["user_id"])

        # Take the user back to the login screen and confirm password change. Also end the current session prompting the user to relogin with the new details
        session.clear()
        flash('Password successfully changed')
        return render_template("login.html")

    # User accessed via GET show them the change password template
    else:
        return render_template("password.html")


# Add route. Allows the user to add their own recipe to the recipes table in the cookbook database
@app.route("/add", methods=["GET", "POST"])
@login_required
def add():

    # User accessed via POST so perform checks and add recipe steps
    if request.method == "POST":

        # Ensure recipe name was submitted
        if not request.form.get("name"):
            flash("Please enter a recipe name")
            return redirect("/add")

        # Ensure recipe time was submitted
        if not request.form.get("time"):
            flash("Please enter a recipe time")
            return redirect("/add")

        # Ensure recipe ingredients was submitted
        if not request.form.get("ingredients"):
            flash("Please enter recipe ingredients")
            return redirect("/add")

        # Ensure recipe type was submitted
        if not request.form.get("type"):
            flash("Please select a recipe type")
            return redirect("/add")

        # Ensure recipe howto was submitted
        if not request.form.get("howto"):
            flash("Please enter a recipe How To description")
            return redirect("/add")

        # Set variables from form inputs
        name = request.form.get("name")
        time = request.form.get("time")
        ingredients = request.form.get("ingredients")
        type = request.form.get("type")
        howto = request.form.get("howto")
        id = session["user_id"]

        # Query database for username
        rows = db.execute("SELECT * FROM recipes WHERE name = ?", name)

        # Prompt user for new recipe name as already in database
        if len(rows) == 1:
            flash("Recipe name already exists. Please select another name")
            return redirect("/add")

        # Insert the recipe into the cookbook database / recipes table
        db.execute("INSERT INTO recipes (id, name, time, ingredients, type, howto) VALUES (?, ?, ?, ?, ?, ?)",
                   id, name, time, ingredients, type, howto)

        # Show confirmation and return user to the add recipe page
        flash('Recipe successfully added!')
        return redirect("/add")

    # User accessed via GET show them the add recipe template
    else:
        return render_template("add.html")


# Update route. Allows the user to input updates to a recipe that they have personally added to the recipes table in the cookbook database
@app.route("/update", methods=["GET", "POST"])
@login_required
def update():

    # User accessed via POST so perform checks and update select recipe steps
    if request.method == "POST":

        # Ensure all fields were submitted and if not return user to the update page with the current recipe information
        if not request.form.get("name") or not request.form.get("time") or not request.form.get("ingredients") or not request.form.get("type") or not request.form.get("howto"):
            recipes = db.execute("SELECT * FROM recipes WHERE name = ?", request.form.get("recipename"))
            flash("Please make sure all fields are filled in")
            return render_template("update.html", recipes=recipes)

        # Set variables from form inputs
        recipename = request.form.get("recipename")
        name = request.form.get("name")
        time = request.form.get("time")
        ingredients = request.form.get("ingredients")
        type = request.form.get("type")
        howto = request.form.get("howto")
        id = session["user_id"]

        # Insert the recipe into the cookbook database / recipes table
        db.execute("UPDATE recipes SET name = ?, time = ?, ingredients = ?, type = ?, howto = ? WHERE name = ? AND id = ?",
                   name, time, ingredients, type, howto, recipename, id)
        flash("Recipe updated")
        return redirect("/updateselect")

    # User accessed via GET show them the update recipe page
    else:
        return redirect("/updateselect")


# Updateselect route. Allows the user to select a recipe they have personally added to update
@app.route("/updateselect", methods=["GET", "POST"])
@login_required
def updateselect():

    # User accessed via POST so perform checks and update select recipe steps
    if request.method == "POST":

        # Ensure recipe name was submitted
        if not request.form.get("name"):
            flash("Please enter the name of the recipe you wish to update")
            return redirect("/updateselect")

        # Query database for username
        recipes = db.execute("SELECT * FROM recipes WHERE name = ?", request.form.get("name"))

        # Prompt user for new recipe name as already in database
        if len(recipes) != 1:
            flash('Recipe not found')
            return redirect("/updateselect")

        # Take the user to the update page and show the chosen recipes current information
        return render_template("update.html", recipes=recipes)

    # User accessed via GET show them the update select recipe template
    else:
        return render_template("updateselect.html")


# Delete route. Allows the user to delete a recipe they have personally added
@app.route("/delete", methods=["POST"])
@login_required
def delete():

    # Create variable from page for item to delete
    name = request.form.get("delete")

    # If the recipe exists delete it from the table
    if name:
        db.execute("DELETE FROM recipes WHERE name = ?", name)
        flash('Successfully deleted')
        return redirect("/account")

    # Take the user back to their account page
    return redirect("/account")


# Account route. Allows the user to view their personally added recipes
@app.route("/account")
@login_required
def account():

    # Caputre the logged in users id
    id = id = session["user_id"]

    # Query the database for all the recipes the user has added
    recipes = db.execute("SELECT * FROM recipes WHERE id = ?", id)

    # Display the results to the user with the option to delete them
    return render_template("account.html", recipes=recipes)


# Recipes route. Allows user to view a carousel of all the recipes available in the database
@app.route("/recipes", methods=["GET", "POST"])
@login_required
def recipes():

    # User accessed via POST so perform checks and add recipe to favorites database
    if request.method == "POST":

        # Create variable from page for item to favorite
        name = request.form.get("favorite")

        # Caputre the logged in users id and query database
        id = id = session["user_id"]
        favorites = db.execute("SELECT * FROM favorites WHERE id = ? AND recipename =?", id, name)

        # Check to see if user has already made a favorite of this recipe
        if len(favorites) == 1:
            flash("Recipe already in favorites")
            return redirect("/recipes")

        # Insert the recipe into the favorites table and update the likes totals
        else:
            db.execute("INSERT INTO favorites (id, recipename) VALUES (?, ?)", id, name)
            db.execute("UPDATE recipes SET likes = likes + 1 WHERE name = ?", name)
            flash('Recipe added to favorites')
            return redirect("/recipes")

    # Query the database for all the recipes available
    else:
        recipes = db.execute("SELECT * FROM recipes")
        return render_template("recipes.html", recipes=recipes)


# Favorites route. Allows the user to view their currently saved favorite recipes in a carousel
@app.route("/favorites", methods=["GET", "POST"])
@login_required
def favorites():

    # Caputre the logged in users id
    id = id = session["user_id"]

    # User accessed via POST so perform checks and remove recipe from favorites database
    if request.method == "POST":

        # Create variable from page for item to remove from favorites
        name = request.form.get("favorite")

        # If the recipe exists delete it from the table
        if name:
            db.execute("DELETE FROM favorites WHERE recipename = ? AND id = ?", name, id)
            db.execute("UPDATE recipes SET likes = likes - 1 WHERE name = ?", name)
            flash('Successfully removed from favorites')
            return redirect("/favorites")

    # Query the database for all the recipes available and take the user back to the favorites page
    else:
        recipes = db.execute("SELECT * FROM recipes WHERE name IN (SELECT recipename FROM favorites WHERE id = ?)", id)
        return render_template("favorites.html", recipes=recipes)


# Vegetarian route. Allows the user to view only the recipes marked type Vegetarian in a carousel
@app.route("/vegetarian", methods=["GET", "POST"])
@login_required
def vegetarian():

    # User accessed via POST so perform checks and add recipe to favorites database
    if request.method == "POST":

        # Create variable from page for item to favorite
        name = request.form.get("favorite")

        # Caputre the logged in users id
        id = id = session["user_id"]
        favorites = db.execute("SELECT * FROM favorites WHERE id = ? AND recipename =?", id, name)

        # Check to see if user has already made a favorite of this recipe
        if len(favorites) == 1:
            flash("Recipe already in favorites")
            return redirect("/vegetarian")

        # Insert the recipe into the favorites table and updates the likes total
        else:
            db.execute("INSERT INTO favorites (id, recipename) VALUES (?, ?)", id, name)
            db.execute("UPDATE recipes SET likes = likes + 1 WHERE name = ?", name)
            flash('Recipe added to favorites')
            return redirect("/vegetarian")

    # Query the database for all the recipes available that are type Vegetarian
    else:
        recipes = db.execute("SELECT * FROM recipes WHERE type = 'Vegetarian'")
        return render_template("vegetarian.html", recipes=recipes)


# Vegan route. Allows the user to view only the recipes marked type Vegan in a carousel
@app.route("/vegan", methods=["GET", "POST"])
@login_required
def vegan():

    # User accessed via POST so perform checks and add recipe to favorites database
    if request.method == "POST":

        # Create variable from page for item to favorite
        name = request.form.get("favorite")

        # Caputre the logged in users id
        id = id = session["user_id"]
        favorites = db.execute("SELECT * FROM favorites WHERE id = ? AND recipename =?", id, name)

        # Check to see if user has already made a favorite of this recipe
        if len(favorites) == 1:

            flash("Recipe already in favorites")
            return redirect("/vegan")

        # Insert the recipe into the favorites table and updates the likes total
        else:
            db.execute("INSERT INTO favorites (id, recipename) VALUES (?, ?)", id, name)
            db.execute("UPDATE recipes SET likes = likes + 1 WHERE name = ?", name)
            flash('Recipe added to favorites')
            return redirect("/vegan")

    # Query the database for all the recipes available that are type Vegan
    else:
        recipes = db.execute("SELECT * FROM recipes WHERE type = 'Vegan'")
        return render_template("vegan.html", recipes=recipes)


# Top5 route. Allows the user to view only the top 5 recipes ranked by number of likes in a carousel
@app.route("/top5", methods=["GET", "POST"])
@login_required
def top5():

    # User accessed via POST so perform checks and add recipe to favorites database
    if request.method == "POST":

        # Create variable from page for item to favorite
        name = request.form.get("favorite")

        # Caputre the logged in users id
        id = id = session["user_id"]

        favorites = db.execute("SELECT * FROM favorites WHERE id = ? AND recipename =?", id, name)

        # Check to see if user has already made a favorite of this recipe
        if len(favorites) == 1:

            flash("Recipe already in favorites")
            return redirect("/top5")

        # Insert the recipe into the favorites table and update the likes total
        else:
            db.execute("INSERT INTO favorites (id, recipename) VALUES (?, ?)", id, name)
            db.execute("UPDATE recipes SET likes = likes + 1 WHERE name = ?", name)
            flash('Recipe added to favorites')
            return redirect("/top5")

    # Query the database for all the recipes available and order them by likes showing only the top 5 results
    else:
        recipes = db.execute("SELECT * FROM recipes ORDER BY likes DESC LIMIT 5")
        return render_template("top5.html", recipes=recipes)