from wsgiref import validate
from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route('/recipes/new')
def create_recipe():
    return render_template("new.html")

@app.route('/recipes/submit', methods=['POST'])
def submit_new_recipe():
    if "user_id" not in session:
        return redirect('/')
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "date_cooked": request.form["date_cooked"],
        "under_30": request.form["under_30"],
        "users_id": session["user_id"]           #<<<<<-----<<<<MY DUH ERROR KEEP EYE next time
    }
    # print(data)
    # print(f"******* {data} *******")
    if not Recipe.validate_recipe(data):
        return redirect("/recipes/new")

    Recipe.save(data)
    return redirect('/main')



@app.route('/show/recipe/<int:id>')
def show_recipe(id):
    data = {
        "id": session['user_id']
    }
    user_in_db = User.get_one_by_id(data)

    one_recipe = Recipe.get_one_recipe({"id":id})
    all_recipes = Recipe.get_all()

    user_data = {
        "id": one_recipe.users_id            #<<<<----------<<<<< MY DUH ERROR
    }

    # print(f"****************    {one_recipe.users_id}   *******************")


    user = User.get_one_by_id(user_data)
    return render_template("show.html", user_in_db=user_in_db, one_recipe=one_recipe, all_recipes=all_recipes, user=user)


@app.route('/delete/<int:id>')
def delete_recipe(id):
    print(f"****** delete recipe {id} *******")

    data = {
        "id":id
    }
    Recipe.delete_recipe(data)
    return redirect("/main")

@app.route('/edit/recipes/<int:id>')
def edit_recipe(id):
    one_recipe = Recipe.get_one_recipe({"id":id})

    return render_template("edit.html", one_recipe=one_recipe)

@app.route('/update/recipe/<int:id>', methods=['POST'])
def update_recipe(id):
    print(f"******* edit recipe {id} *******")
    
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "date_cooked": request.form["date_cooked"],
        "under_30": request.form["under_30"],
        "id": id
    }

    print(f"******* edit recipe {data} *******")
    Recipe.edit_recipe(data)
    return redirect('/main')      