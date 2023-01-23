# The Community Cookbook
### Video Demo:  <https://youtu.be/_THg0wRDZl8>
### Description: CS50 Final Project The Community Cookbook

#### The Idea
The idea for the community cookbook came about after i recently moved to a new country and decided to focus more on my homecooked meals rather than ordering too much takeout. I had been visiting my family and trying to source recipes that i had shared with them in the past. When the CS50 project came about i thought of the idea of making this process easier and the communuity cookbook project was born.

### The Design
The design for the community cookbook was about keeping things simple and concise. Too many times I wasted a whole evening just trying to find a recipe sorting through multiple webpages with too much clutter. I wanted to give the user the ability to not only browse recipes, but interact with the web application and be able to favorite, filter and add their own recipes. The design choice to add filters for the vegetarian and vegan options came from my sister, who is a vegan, who said she expected this sort of filtering as mandatory in todays age rather than optional so i wanted to make sure this was included. The Top 5 recipes design choice was a personal one when considering how I would personally navigate the site. I am very undecisive and this option just seemed to make sense to allow me a good place to start based on other users feedback. The final design choice of note was that of the option to update a recipe you have already added. The first iteration of this was to create a smiliar page to the add recipe page that instead of the INSERT command into the database it just used the UPDATE command instead. But when testing this I realized that i was being prompted to insert all the recipe information again just to update one thing. I changed this part of the design so that the user is first prompted to select a recipe to update and are then presented with the current recipe information. From this point they can change as little as they need and the rest of the information is just saved again. This saves the user time and frustation and would have been an easy oversight.

### The Implementation
The project contains two python files. The first is the main app.py file and the second is the helpers.py file.

The helpers.py file contains the login_required function that requires users to be logged in to view a page and is borrowed from the PSET9 finance problem.

The app.py files contains all the functions creating the interativity of the web application. These are;
- After_request: Borrowed from PSET9 finance. After each route request it will ensure the responses aren't cached.
- Index: Index route or homepage for the application. Simply takes the user to homepage of the web app.
- Login: Login route. Allows the user to login via POST or visit the login page via GET. Login will check the users details are in the database and create a session for the associated user id.
- Logout: Login route. Allows the user to logout of clear the current session.
- Register: Register route. Allows the user to register for the web app and save their details into the users table in the cookbook database.
- Password: Password route. Allows the user to change their current password in the database.
- Add: Add route. Allows the user to add their own recipe to the recipes table in the cookbook database.
- Update: Update route. Allows the user to input updates to a recipe that they have personally added to the recipes table in the cookbook database.
- Updateselect: Updateselect route. Allows the user to select a recipe they have personally added to update.
- Delete: Delete route. Allows the user to delete a recipe they have personally added.
- Account: Account route. Allows the user to view their personally added recipes.
- Recipes: Recipes route. Allows user to view a carousel of all the recipes available in the database.
- Favorites: Favorites route. Allows the user to view their currently saved favorite recipes in a carousel.
- Vegetarian: Vegetarian route. Allows the user to view only the recipes marked type Vegetarian in a carousel.
- Vegan: Vegan route. Allows the user to view only the recipes marked type Vegan in a carousel.
- Top5: Top5 route. Allows the user to view only the top 5 recipes ranked by number of likes in a carousel.

The static folder contains a number of static images used on the web app along with the styles.css file. This file contains several CSS properties that define the style of several items throughout the application. These include but are not limited to text sizing and creating margins on different objects throughout.

The templates folder contains all the HTML documents for the pages used throughout the web application. The layout.html file contains the header and footer and used throughout where as the other individual html files all extend this layout. Some of the main features in the html files are the Carousel feature from the Bootstrap library. The Naviagation bar from the Bootstrap library. Many forms, tables and buttons are used throughout to create the interactive experience for the user.

The project contains the cookbook.db database which is the main and only database used by the web application. It has three tables which are;
- Users: This table contains information on the registered users of the web application. The columns are the name of the user, an individual id for the user and the users password saved as a hash.
- Favorites: This table contains the favorite recipes saved by the user. The columns are the users id and the recipes name.
- Recipes: This table contains the information added for the recipe. The columns are the id of the user who added the recipe, the recipe name, time, ingredients, type, a How To and the current number of likes that recipe has.

The project contains a requirements.txt file that shows all the projects library dependancies.

The project contains a flask_session folder that is used by the funcationality to create a session for the user.

The project finally contains this READEME which describes the project in detail.

### Future Prospects
Although the current state of the web application is what will be uploaded as my CS50 Final Project I had several ideas for future implementations. These include;
- More filtering options on the recipe page such as gluten and other sensitivities.
- Possibility to pull nutrition data from a open source API that can help the user track nutrition details of their meals.
- Finally implementing a recipe of the week or a highlighting of a users top recipe for others to see. I beleive the idea of this web application allows for endless ways to improve and creates a final product that leaves future development avenues open.