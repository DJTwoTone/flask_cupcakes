"""Flask app for Cupcakes"""

from flask import Flask, jsonify, request, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
# db.create_all()

# from flask_debugtoolbar import DebugToolbarExtension
# app.config['SECRET_KEY'] = 'yummyyummyinmytummy'
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app)

def serialize_cupcake(cupcake):
    """Serialize a cupcake object to a dictionary"""
    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image,
    }


@app.route('/api/cupcakes')
def all_cupcakes():

    cupcakes = Cupcake.query.all()
    serial_cupcakes = [serialize_cupcake(d) for d in cupcakes]

    return jsonify(cupcakes=serial_cupcakes)

@app.route('/api/cupcakes/<cupcake_id>')
def single_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serial_cupcake = serialize_cupcake(cupcake)

    return jsonify(cupcake=serial_cupcake)

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serial_cupcake = serialize_cupcake(new_cupcake)

    return ( jsonify(cupcake=serial_cupcake), 201 )

@app.route('/api/cupcakes/<cupcake_id>', methods=["PATCH"])
def update_cupcake(cupcake_id):

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)

    db.session.commit()
    serial_cupcake = serialize_cupcake(cupcake)

    return jsonify(cupcake=serial_cupcake)

@app.route('/api/cupcakes/<cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")

@app.route("/")
def home():

    return render_template('index.html')