from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import user_model
from flask import flash

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30_minutes = data['under_30_minutes']
        self.date_cooked = data['date_cooked']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

# *******- selects all recipes and shows in recipes -****************
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(DATABASE).query_db(query)
        recipes = []
        for r in results:
            print(r)
            recipes.append(cls(r))
        return recipes

# *******- creates/inserts one recipe -****************
    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, under_30_minutes, date_cooked, user_id) VALUES (%(name)s, %(description)s, %(instructions)s,%(under_30_minutes)s,%(date_cooked)s, %(user_id)s);"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

# *******- gets the one recipe from the one user -****************
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes left join users on recipes.user_id = users.id where recipes.id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        one_recipe = cls(result[0])

        user_data = {
                "id" : result[0]["users.id"],
                "first_name": result[0]['first_name'],
                "last_name": result[0]['last_name'],
                "email": result[0]['email'],
                "password": result[0]['password'],
                "created_at": result[0]['users.created_at'],
                "updated_at": result[0]['users.updated_at']
        }

        one_recipe.owner = user_model.User(user_data)
        return one_recipe

# *******- Updates/edits the recipe  -****************
    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name=%(name)s, description = %(description)s, instructions = %(instructions)s, under_30_minutes = %(under_30_minutes)s, date_cooked = %(date_cooked)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

# *******- deletes the recipe -****************
    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

# *******- allows the recipe selected to be displayed -****************   
    @classmethod
    def get_recipe_by_id(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validates_recipe_creation_updates(data):
        is_valid = True
# *******- validates recipe name -****************
        if len(data['name']) == 0:
            flash("Please provide a recipe name!")
            is_valid = False
        if len(data["name"]) < 3:
            flash("Recipe name must be at least three characters")
            is_valid = False

# *******- validates recipe description -****************
        if len(data['description']) == 0:
            flash("Please provide a description!")
            is_valid = False
        if len(data["description"]) < 3:
            flash("Description must be at least three characters")
            is_valid = False

# *******- validates recipe instructions -****************
        if len(data['instructions']) == 0:
            flash("Please provide instructions!")
            is_valid = False
        if len(data["instructions"]) < 3:
            flash("Instructions must be at least three characters")
            is_valid = False

# *******- validates recipe under 30 minutes -****************
        if 'under_30_minutes' not in data:
            flash("Under 30 minutes required!")
            is_valid = False

# *******- validates recipe date that was cooked -****************
        if  not data['date_cooked']:
            flash("Date made required!")
            is_valid = False

        return is_valid