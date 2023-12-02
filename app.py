import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import certifi

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
app = Flask(__name__)

cxn_str = 'mongodb+srv://yourn:Moran_21@cluster0.crlkgld.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(cxn_str)
db = client.dbsparta_plus_week3

MONGODB_URI = MongoClient("mongodb+srv://yourn:Moran_21@cluster0.crlkgld.mongodb.net/?retryWrites=true&w=majority")
DB_NAME =  os.environ.get("client.dbsparta_plus_week3")


@app.route('/')
def main():
    return render_template("index.html")

@app.route('/restaurants', methods=["GET"])
def get_restaurants():
    # This api endpoint should fetch a list of restaurants
    restaurants = list(db.restaurant.find({}, {'_id': False}))
    return jsonify({
        'result': 'success', 
        'restaurants': restaurants,
        })


@app.route('/map')
def map_example():
    return render_template("prac_map.html")

@app.route('/restaurant/create', methods=['POST'])
def create_restaurant():
    name = request.form.get('name')
    categories = request.form.get('categories')
    location = request.form.get('location')
    longitude = request.form.get('longitude')
    latitude = request.form.get('latitude')
    doc = {
        'name': name,
        'categories': categories,
        'location': location,
        'center': [longitude, latitude],
    }
    db.restaurant.insert_one(doc)
    return jsonify({
        'result': 'success',
        'msg': 'successfully created a restaurant'
    })

@app.route('/restaurant/delete', methods=['POST'])
def delete_restaurant():
    name = request.form.get('name')
    db.restaurant.delete_one({'name': name})
    return jsonify({
        'result': 'success',
        'msg': 'successfully delete a restaurant'
    })

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)