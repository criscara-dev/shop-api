from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from models.item import ItemModel

class Item(Resource):  
    
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json()
        return {'message':'Item not found'}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {f'message': "An item with name '{self.name}' already exists."}, 400 # error with the request
        
        data = Item.parser.parse_args()

        item = ItemModel('name',data['price']) 
        try:
            item.insert()
        except:
            return {'message':'An error occurred inserting the item.'}, 500 # internal server error
        
        return item.json(), 201

   
    
    # to delete an item I have to ricreate the list without the one I want to get rid. Weird.
    @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()
        
        return {'message': 'Item deleted'}
    
    @jwt_required()
    # is idempotent: it create (if the item does not exist) or update
    def put(self, name):
        data = Item.parser.parse_args()
        # Once again, print something not in the args to verify everything works
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel('name',data['price']) 

        if item is None:
            try:
                updated_item.insert()
            except:
                return {'message':'An error occurred inserting the item.'}, 500
        else:
            try:
                updated_item.update()
            except:
                return {'message':'An error occurred updating the item.'}, 500
        return updated_item.json()

    

class ItemList(Resource):

    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)

        items = []
        for row in result:
            items.append({'name':row[0],'price':row[1]})
        connection.close()

        return {'items':items}