from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Instantiate app and db at top-level
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # or your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)

# Import your models here AFTER db is initialized
from models import Plant

# Set up routes here
@app.route('/plants')
def get_plants():
    plants = Plant.query.all()
    return [plant.to_dict() for plant in plants]  # Use your own to_dict method

@app.route('/plants/<int:id>')
def get_plant_by_id(id):
    plant = Plant.query.get_or_404(id)
    return plant.to_dict()

@app.route('/plants', methods=['POST'])
def create_plant():
    from flask import request
    data = request.get_json()
    plant = Plant(
        name=data['name'],
        image=data.get('image'),
        price=data.get('price'),
    )
    db.session.add(plant)
    db.session.commit()
    return plant.to_dict(), 201
