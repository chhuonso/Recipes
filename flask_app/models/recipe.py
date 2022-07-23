from wsgiref import validate
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User
DATABASE = "recipes_users"

class Recipe: 
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.under_30 = data["under_30"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.date_cooked = data["date_cooked"]
        self.users_id = data["users_id"]
        self.poster = None
    

    # The validate on the form
    @staticmethod
    def validate_recipe(recipe_form): 
        is_valid = True # ! assume this is true

        if len(recipe_form['name']) < 2:
            flash("Name must be at least 2 characters.")
            is_valid = False
        if len(recipe_form['description']) < 2:
            flash("Description must be at least 2 characters.")
            is_valid = False
        if len(recipe_form['instructions']) < 2: 
            flash("Instructions must be at least 2 characters.")
            is_valid = False
        return is_valid


    @classmethod        # get all from data
    def get_all(cls):
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.users_id"
        results = connectToMySQL(DATABASE).query_db(query)
        print(results)

        all_recipes = []        #STORE DATA TO NEW VARIABLE IN THE ARRAY using push/append

        for recipe in results:         
            single_recipe = cls(recipe)    #each class name or data thats needed

            user_data = {
                "id": recipe["users.id"],
                "first_name": recipe["first_name"],
                "last_name": recipe["last_name"],
                "email": recipe["email"],
                "password": recipe["password"],
                "created_at": recipe["users.created_at"],
                "updated_at": recipe["users.updated_at"]
            }
            single_recipe.poster = User(user_data)
            all_recipes.append(single_recipe)
        return all_recipes


    #CRUD
    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (name,under_30,description,instructions,date_cooked,created_at,updated_at,users_id) VALUES(%(name)s,%(under_30)s, %(description)s,%(instructions)s,%(date_cooked)s,NOW(),NOW(),%(users_id)s)"

        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_one_recipe(cls, data):
        query = "SELECT * FROM recipes WHERE id=%(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        
        one_recipe = cls(results[0])
        return one_recipe
    
    @classmethod
    def edit_recipe(cls, data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, under_30=%(under_30)s, instructions=%(instructions)s, date_cooked=%(date_cooked)s, updated_at=NOW() WHERE id=%(id)s"

        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id=%(id)s"

        return connectToMySQL(DATABASE).query_db(query, data)
    

