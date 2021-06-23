from flask import Flask, request
from flask_restful import Api
from flask_jwt import JWT

from user import User, UserRegister
from security import identity, authenticate
from item import Item, ItemList

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True # To allow flask propagating exception even if debug is set to false on app
app.secret_key = 'mySecretKey'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # implement: /auth



api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    app.run(debug=True)  # important to mention debug=True
