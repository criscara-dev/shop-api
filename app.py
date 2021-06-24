from flask import Flask, request
from flask_restful import Api
from flask_jwt import JWT
from db import db


from resources.user import UserRegister
from security import identity, authenticate
from resources.item import Item, ItemList


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True # To allow flask propagating exception even if debug is set to false on app
app.secret_key = 'mySecretKey'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # implement: /auth



api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
