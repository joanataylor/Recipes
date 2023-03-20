from flask_app.models.recipe_model import Recipe
from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models import user_model

# *******- routes to page that shows all recipes -****************
@app.route("/recipes")
def dashboard():
    if not 'uid' in session:
        flash("access denied")
        return redirect("/")
    results = user_model.User.all_recipes_with_users()
    print(results)
    print(session['uid'])
    return render_template('recipes.html', results=results)

# @app.route("/all/recipe")
# def creating():
#     results = Recipe.save()
#     return render_template('create_recipe.html', results=results)


@app.route("/recipe/all")
def all_recipes():
    return render_template('create_recipe.html', all_recipes=Recipe.get_all())

@app.route('/recipes/destroy/<int:id>')
def distroy_recipes(id):
    data = {
        "id": id
    }
    recipes = Recipe.destroy(data)
    return redirect("/recipes")

@app.route('/recipes/display/<int:id>')
def display_recipes(id):
    data = {
        "id": id
    }
    recipes = Recipe.get_one(data)
    return render_template('show_recipe.html', recipes = recipes)

@app.route('/recipes/edit/<int:id>')
def edit_recipes(id):

    data = {
        "id": id
    }
    result = Recipe.get_recipe_by_id(data)
    return render_template('edit_recipe.html', result = result)


@app.route("/create_recipe", methods=["POST"])
def new_recipe():

    if not Recipe.validates_recipe_creation_updates(request.form):
        return redirect("/recipe/all")

    data={
        **request.form,
        "under_30_minutes": int(request.form['under_30_minutes']),
        "user_id": session['uid']
    }
    Recipe.save(data)
    return redirect("/recipes")

@app.route("/edit_recipes/<int:id>", methods=["POST"])
def updated_recipe(id):

    if not Recipe.validates_recipe_creation_updates(request.form):
        return redirect("/recipes/edit/"+str(id))

    data={
        **request.form,
        "under_30_minutes": int(request.form['under_30_minutes']),
        "id": id
    }
    Recipe.update(data)
    return redirect("/recipes")

# @app.route('/new_user', methods=['POST'])
# def new_user():


#     register_check = User.validate(request.form)
#     if not register_check:
#         return redirect('/')

#     hash = bcrypt.generate_password_hash(request.form['password'])

#     data = {
#         "first_name": request.form['first_name'],
#         "last_name": request.form['last_name'],
#         "email": request.form['email'],
#         "password": hash
#     }

#     User.register(data)
#     return redirect("/")




    # edit_recipe_check = Recipe.validates_recipe_creation_updates(request.form)
    # if not edit_recipe_check:
    #     return('/recipes/edit/<int:id>')