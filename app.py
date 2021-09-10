from flask import Flask, Blueprint
from admin import admin
from auth import auth

#Main Page
app=Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.register_blueprint(auth)
app.register_blueprint(admin)



if __name__ == '__main__':
    app.run(debug=True)

   






