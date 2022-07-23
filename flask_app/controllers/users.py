from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index_login_reg_page():
    if "user_id" in session:
        del session["user_id"]
    return render_template('login.html')


#adds new user to the list in the data and bcrypt there password
@app.route("/users/register", methods=["POST"])
def register_user():
    if not User.validate_user(request.form):
        print("Not Valid")
        return redirect("/")
    data = {
        "email": request.form["email"]
    }
    user_in_db = User.get_one_by_email(data)
    if  user_in_db:
        flash("Email already in use!")
        return redirect("/")
    else:
        print("It's VALID")
        pw_hash = bcrypt.generate_password_hash(request.form["password"]) # says it all here/ bcrypt password
        # print(pw_hash)
        data ={
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "password": pw_hash,
            "email": request.form["email"],
        }
        #Register new user
        user_id = User.save(data)     
        # print(f"Your new user has id: {user_id}")
        session["user_id"] = user_id #personal data of this users i.e(likes/cart/poster)
    return redirect("/main")

# checks if user email or password is correct and will be loggeed in if TRUE
@app.route("/users/login", methods=["POST"])
def login_user():
    print(request.form["email"])
    data = {
        "email": request.form["email"]  
    }
    user_in_db = User.get_one_by_email(data) 
    # print(user_in_db)
    if not user_in_db:
        flash("Invalid email/password otherwise User doesn't exist")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        return redirect('/')
    session["user_id"] = user_in_db.id
    return redirect("/main")  #SUCCESS PAGE-MAIN PAGE OF THE SITE

@app.route("/main")
def recipes_page():
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id": session["user_id"]
    }
    user_in_db = User.get_one_by_id(data) 
    all_recipes = Recipe.get_all()
    return render_template("main.html", user_in_db = user_in_db, all_recipes=all_recipes)

    #now we need to query our recipes and join users from the database NEXT---> (recipe.py create a class Recipe)






