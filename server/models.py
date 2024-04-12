from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Plant(db.Model, SerializerMixin):
    __tablename__ = 'plants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable = False)
    image = db.Column(db.String(120), nullable = True)
    price = db.Column(db.Numeric(10,2), nullable = False)
    
    def to_dict(self):
        return{
            'id': self.name,
            'name': self.name,
            'image': self.image,
            'price': float(self.price)
        }
    @classmethod
    def get_all(cls):
        plants = cls.query.all()
        return jsonify([plant.to_dict() for plant in plants])
    
    @classmethod
    def get_by_id(cls, plant_id):
        plant = cls.query.get(plant_id)
        if plant:
            return jsonify(plant.to_dict())
        else:
            return jsonify({'error': 'Plant not found'}), 404
    
    @classmethod
    def create(cls):
        data = request.get_json()
        plant =cls(name=data['name'], image=data['image'], price=data['price'])
        db.session.add(plant)
        db.session.commit()
        return jsonify(plant.to_dict()), 201
