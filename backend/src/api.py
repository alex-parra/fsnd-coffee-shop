import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

# db_drop_and_create_all()

# ROUTES
@app.route('/')
def index():
    return jsonify({'/drinks': 'List drinks'})


'''
GET /drinks
    it should be a public endpoint
    it should contain only the drink.short() data representation
returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
    or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def list_drinks():
    return jsonify({'success': True, 'drinks': [d.short() for d in Drink.query.all()]})


'''
GET /drinks-detail
    it should require the 'get:drinks-detail' permission
    it should contain the drink.long() data representation
returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
    or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
def list_drinks_detailed():
    return jsonify({'success': True, 'drinks': [d.long() for d in Drink.query.all()]})


'''
POST /drinks
    it should create a new row in the drinks table
    it should require the 'post:drinks' permission
    it should contain the drink.long() data representation
returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
    or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
# TODO: require auth with post:drinks
def create_drink():
    title = request.json.get('title', None)
    recipe = request.json.get('recipe', None)

    byTitle = Drink.query.filter(Drink.title == title).all()
    if len(byTitle):
        return abort(422)

    # TODO: Validate data

    newDrink = Drink(title=title, recipe=json.dumps(recipe))
    newDrink.insert()
    return jsonify({'success': True, 'drinks': [newDrink.long()]})


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
# TODO: require auth with patch:drinks
def update_drink(id):
    drink = Drink.query.get(id)
    if drink is None:
        return abort(404)

    drinkInfo = drink.long()
    recipe = request.json.get('recipe', drinkInfo['recipe'])
    drink.title = request.json.get('title', drinkInfo['title'])
    drink.recipe = json.dumps(recipe)
    drink.update()
    return jsonify({'success': True, 'drinks': [drink.long()]})


'''
DELETE /drinks/<id>
    where <id> is the existing model id
    it should respond with a 404 error if <id> is not found
    it should delete the corresponding row for <id>
    it should require the 'delete:drinks' permission
returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
    or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
# TODO: require auth with delete:drinks
def delete_drink(id):
    drink = Drink.query.get(id)
    if drink is None:
        return abort(404)

    drink.delete()
    return jsonify({'success': True, 'delete': drink.id})


# Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
error handler should conform to general task above 
'''
@app.errorhandler(404)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


'''
error handler should conform to general task above 
'''
@app.errorhandler(401)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "unauthorized"
    }), 401
