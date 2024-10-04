
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from models import db, connect_db, Cupcake
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_ECHO'] = True

app.app_context().push()
connect_db(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "11wondersoftheworld"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False



@app.route("/")
def root():
    """Render homepage."""

    return render_template("index.html")

@app.route('/api/cupcakes')
def list_cupcakes():
    """Returns JSON w/ all cupcakes"""
    all_cupcakes = [cupcakes.serialize() for cupcakes in Cupcake.query.all()]

    # cupcakes = [cupcake.to_dict() for cupcake in Cupcake.query.all()]
  
    return jsonify(cupcakes=all_cupcakes)


@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    """Returns JSON for one cupcake in particular

    Returns JSON like:
        {cupcake: [{id, flavor, rating, size, image}]}
    """
    a_cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=a_cupcake.serialize())


@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    data = request.json

    cupcake = Cupcake(flavor=data['flavor'],rating=data['rating'],size=data['size'],image=data['image'] or None)

    db.session.add(cupcake)
    db.session.commit()
    return (jsonify(cupcake=cupcake.to_dict()), 201)


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCh'])
def update_cupcake(cupcake_id):
    """Update cupcake and return updated data

    Returns JSON like:
        {cupcake: [{id, flavor, rating, size, image}]}
    """

    data = request.json

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = data['flavor']
    cupcake.rating = data['rating']
    cupcake.size = data['size']
    cupcake.image = data['image']

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.to_dict())


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def remove_cupcake(cupcake_id):
    """Delete cupcake and return confirmation message.

    Returns JSON of {message: "Deleted"}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")




# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5505, debug=True)