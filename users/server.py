from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL    # import the function that will return an instance of a connection
app = Flask(__name__)

@app.route("/users")
def index():
    mysql = connectToMySQL('users_db')	        # call the function, passing in the name of our db
    users = mysql.query_db('SELECT * FROM users;')  # call the query_db function, pass in the query as a string
    print(users)
    return render_template("index.html", all_users=users)

@app.route("/users/new")
def new():
    return render_template("new.html")

@app.route("/users/<id>")
def get_single_user(id):
    mysql = connectToMySQL('users_db')	        # call the function, passing in the name of our db
    query = f"SELECT * FROM users WHERE id = {id};"
    show_user = mysql.query_db(query)
    print(show_user)
    
    return render_template("show.html", one_user = show_user[0])

@app.route("/users/create", methods=['POST'])
def add_new_user():
    mysql = connectToMySQL('users_db')        # call the function, passing in the name of our db
    query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (%(fn)s, %(ln)s, %(em)s, NOW(), NOW());"
    data = {
        "fn": request.form["first_name"],
        "ln": request.form["last_name"],
        "em": request.form["email"]
    }
    new_user_id = mysql.query_db(query, data)
    print(new_user_id)
    return redirect(f"/users/{new_user_id}")

@app.route("/users/<id>/edit")
def edit(id):
    mysql = connectToMySQL('users_db')	        # call the function, passing in the name of our db
    query = "SELECT * FROM users WHERE id = %(id)s;"
    data = {
        "id": id
    }
    edit_user = mysql.query_db(query, data)
    print(edit_user)

    return render_template("edit.html", edit_this_user = edit_user[0], id = id)

@app.route("/users/<id>/update", methods=["POST"])
def update(id):
    print("HEllp??????????????")
    mysql = connectToMySQL('users_db')        # call the function, passing in the name of our db
    query = "UPDATE users SET first_name = %(fn)s, last_name = %(ln)s, email = %(em)s, updated_at = NOW() WHERE id = %(id)s;"
    data = {
        "fn": request.form["first_name"],
        "ln": request.form["last_name"],
        "em": request.form["email"],
        "id": id
    }
    mysql.query_db(query, data)
    return redirect(f"/users/{id}")

@app.route("/users/<id>/destroy")
def delete(id):
    print("We in here")
    mysql = connectToMySQL('users_db')	        # call the function, passing in the name of our db
    query = "DELETE FROM users WHERE id = %(id)s;"
    data = {
        "id": id
    }
    delete_user = mysql.query_db(query, data)
    print(delete_user)

    return redirect("/users")
            
if __name__ == "__main__":
    app.run(debug=True)