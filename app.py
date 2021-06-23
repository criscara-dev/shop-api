from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required, current_identity

from security import identity, authenticate

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True # To allow flask propagating exception even if debug is set to false on app
app.secret_key = 'mySecretKey'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # implement: /auth

items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    

    @jwt_required()
    def get(self, name):
        # nect can break to code so add a second defalut parameter as None
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {"item":item}, 200 if item else 404

    @jwt_required()
    def post(self, name):
        data = Item.parser.parse_args()
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {f'message': "An item with name '{name}' already exists."}, 400
            
        item = {'name': name,'price': data['price']} 
        items.append(item)
        return item, 201
    
    # to delete an item I have to ricreate the list without the one I want to get rid. Weird.
    @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}
    
    @jwt_required()
    # is idempotent: it create (if the item does not exist) or update
    def put(self, name):
        data = Item.parser.parse_args()
        # Once again, print something not in the args to verify everything works
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return {"items":items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')


if __name__ == '__main__':
    app.run(debug=True)  # important to mention debug=True