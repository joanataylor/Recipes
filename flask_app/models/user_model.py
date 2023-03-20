from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, request
from flask_app.models.recipe_model import Recipe


from flask_app import DATABASE, bcrypt


import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

# *******- my constructor for my users table - -****************
# *******- this will match all info from Database Users Table -****************
class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.recipes = [] #<---- *******- creates an empty array for all the recipes to exist from each user -****************

# *******- Adds the registered user to the database -****************
# *******- Asks the database to register the values received from the form -****************
# *******- returns(saves in database) the data inserted -****************
    @classmethod
    def register(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s,%(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query,data)

# *******- finds user by email for login form -****************
# *******- def name is anything i want it to be and inside parens(i pass in cls-the constructor- and data is from the query I made from Database) -****************
# *******- searches for email in database -****************
# *******- creates a variable named results to store the email found in the database -****************
# *******- if email(results) found in database exists(bigger than 0) -****************
# *******- creates a variable named found_user that stores the 1st result found(index 0) -****************
# *******- if results returns anything it returns the user found(the email is found) -****************
# *******- if results does NOT returns anything it returns FALSE - meaning email does not exist in database -****************
    @classmethod
    def find_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results and len(results) > 0:
            found_user = cls(results[0])
            return found_user
        else:
            return False

# ???????????????- Do i need this class method if i'm validating at the bottom?-??????????????????????????
# *******- checks email duplication for registration form -****************
# *******- doesn't allow user to register with an existing email -****************
# *******- sets a varible to equal a bool True-****************
# *******- searches database for email -****************
# *******- sets a variable (results) to carry the data received from database -****************
# *******- if the email is NOT in the results received -****************
# *******- the user can go ahead and register the email provided -****************
# *******- or if the email recieved from the form IS IN results that provided from database then it flashes 'email already in use!' -****************
# *******- do i need the last return is_valid statement? if its already being returned valid in 4 lines above? -****************
    @classmethod
    def unique_email(cls, data):
        is_valid = True

        query = "SELECT email FROM users WHERE email = %(email)s;"

        results = connectToMySQL(DATABASE).query_db(query, data)

        if not results:
            return is_valid
        elif data['email'] in results[0]['email']:
            flash("Email already in use!")
            is_valid = False
        return is_valid

# *******- validates login - checks if user can login -****************
# *******- function name is anything i want it to be(preferably related to the action) -****************
# *******- set found_user to be the data in classmethod find_by_email(the data that was returned) -****************
# *******- if email that was input doesnt exist in database -****************
# *******- and or if the password that was input doesnt match the hashed password -****************
# *******- it flashes INVALID LOGIN -****************
# *******- if both email is found in database and password matches the emails hashed out password-****************
# *******- approves login and directs to next page-****************
    @classmethod
    def validate_login(cls, data):

        found_user = cls.find_by_email(data)

        if not found_user:
            flash("Invalid login...")
            return False
        elif not bcrypt.check_password_hash(found_user.password, data['password']):
            flash("Invalid login...")
            return False

        return found_user

# ???????- why static method? does that mean in parens i dont pass in cls (is that why its a static?-??????????????????
# *******- validates all the data input while REGISTERING a user -****************
# *******- if it goes through all validations it will return is_valid - meaning its possible to register that user -****************
# *******- if all inputs are up to standards -****************
    @staticmethod
    def validate(data):
        is_valid = True

# *******-  CAN OR SHOULD THE ELIFS BE IFS??????????????????????????????????????????-****************
# *******- validates first name -****************
        if len(data['first_name']) == 0:
            flash("Please provide a first name!")
            is_valid = False
        elif len(data["first_name"]) < 2:
            flash("User first name must be at least two characters")
            is_valid = False
        elif not data['first_name'].isalpha():
            flash("First name must only contain characters")
            is_valid = False

# *******- validates last name -****************
        if len(data['last_name']) == 0:
            flash("Please provide a last name!")
            is_valid = False
        if len(data["last_name"]) < 2:
            flash("User last name must be at least two characters")
            is_valid = False
        if not data['last_name'].isalpha():
            flash("last name must only contain characters")
            is_valid = False

# *******- validates email and password -****************
        if len(data['email']) == 0:
            flash("Please provide an email!")
            is_valid = False
        if len(data["password"]) < 8:
            flash("Password must be at least eight characters")
            is_valid = False
        if data["password"] != data["confirm_password"]:
            flash("Passwords do not match!")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!")
            is_valid = False
        if User.find_by_email(data):
            flash("Email is already registered!")
            is_valid = False

        return is_valid

# *******- is returning only is_valid because variable at the top is already defined as is_valid = True -****************
# *******- it would never reach the end of the ifs if at any point it was returned is_valid = False -****************
# *******- if email provided doesnt match the REGEX way of doing it - states email address is not valid -****************
# *******- checks if it's a unique email address -****************






# *******- JOINS ONE(users) TO MANY(recipes) -****************
# *******- Joins users and recipes together -****************



# *******- this is how to join two tables 1 - many -****************
# *******- displays all the recipes created along with each users name that created it -****************
# *******- DO I NEED BOTH OF THESE CLASS METHODS in order to join tables? -****************
# *******- I don't technically need both but if at any point i want to get all the users with the recipes created i need the get_user_with_recipes -****************
# *******- I definitely need the first one all_recipes_with users -****************
# *******- all_recipes_with_users is used to display all the recipes on my recipes.html page along with the user that created it -****************
# *******- I don't technically need both but if at any point i want to get all the recipes with the user that created it then I need the all_recipes_with_users -****************
    @classmethod
    def all_recipes_with_users(cls):
        query = "SELECT * FROM recipes LEFT JOIN users on recipes.user_id = users.id"
        results = connectToMySQL(DATABASE).query_db( query )
        all_recipes = []
# *******- start of a for loop -****************
        for row in results: # *******- each row(unique id) found in the results received from the database -****************
            one_recipe = Recipe(row)# *******- one_recipe holds the class constructor from class Recipe and in the parens I pass in(row for each row i want to receive)???????????? -****************

            user_data = {
                "id" : row["users.id"],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            one_recipe.owner = cls(user_data)
            all_recipes.append(one_recipe)
# *******- end of the loop -****************
        return all_recipes


# *******- get_user_with_recipes holds the user and its recipes -****************
    @classmethod
    def get_user_with_recipes( cls , data ):
        query = "SELECT * FROM users LEFT JOIN recipes ON users.id = recipes.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db( query , data )

        user = cls( results[0] )
        for row in results:

            recipe_data = {
                "id" : row['id'],
                "name" : row['name'],
                "description" : row['description'],
                "instructions" : row['instructions'],
                "under_30_minutes" : row['under_30_minutes'],
                "date_cooked" : row['date_cooked'],
                "created_at" : row['created_at'],
                "updated_at" : row['updated_at'],
                "user_id" : row['user_id']
            }
            user.recipes.append(Recipe(recipe_data))
        # print(user.recipes)
        return user



#?????????? each time i create a varible named results inside of a classmethod it only counts inside that method, the reason i can use it in the controllers
# is because when i say results i attach the name of the def method used????????

#????? is the cls im passing in the parens the info from the constructor (__init__)????