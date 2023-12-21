"""Flask app for Cupcakes"""
from flask import Flask, request, render_template, flash, redirect, render_template, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cupcakes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/api/cupcakes', methods=["GET"])
def list_all_cupcakes():

    cupcakes = [cupcake.to_dict() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route('/api/cupcakes/<int:cupcake_id>')
def list_cupcake(cupcake_id):
    
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    

    return jsonify(cupcake=cupcake.to_dict())

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():

    data = request.json

    cupcake = Cupcake(
        flavor=data['flavor'],
        rating=data['rating'],
        size=data['size'],
        image=data['image'] or None)

    db.session.add(cupcake)
    db.session.commit()


    return (jsonify(cupcake=cupcake.to_dict()), 201)

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    if 'flavor' in request.json:
        cupcake.flavor = request.json['flavor']
    if 'size' in request.json:
        cupcake.size = request.json['size']
    if 'rating' in request.json:
        cupcake.rating = request.json['rating']
    if 'image' in request.json:
        cupcake.image = request.json['image']

    db.session.commit()

    return jsonify(cupcake=cupcake.to_dict())

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="deleted")

@app.route("/")
def show():

    return render_template("index.html")

    



    

