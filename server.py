from flask_app.controllers import users_controllers, recipes_controllers
from flask_app import app

if __name__=="__main__":
    app.run(debug=True)


# Flash messages in add recipe and Edit recipe stating all fields must NOT be blank