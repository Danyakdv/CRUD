from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Car, User

car_parser = reqparse.RequestParser()
car_parser.add_argument('make', type=str, required=True, help='Марка автомобиля')
car_parser.add_argument('model', type=str, required=True, help='Модель автомобиля')
car_parser.add_argument('year', type=int, required=True, help='Год выпуска автомобиля')

class CarResource(Resource):
    @jwt_required()
    def get(self, car_id=None):
        if car_id:
            car = Car.query.get(car_id)
            if car:
                return {'id': car.id, 'make': car.make, 'model': car.model, 'year': car.year}
            return {'message': 'Автомобиль не найден'}, 404
        else:
            cars = Car.query.all()
            return [{'id': car.id, 'make': car.make, 'model': car.model, 'year': car.year} for car in cars]

    @jwt_required()
    def post(self):
        args = car_parser.parse_args()
        user_id = get_jwt_identity()
        new_car = Car(make=args['make'], model=args['model'], year=args['year'], user_id=user_id)
        db.session.add(new_car)
        db.session.commit()
        return {'id': new_car.id, 'make': new_car.make, 'model': new_car.model, 'year': new_car.year}, 201

    @jwt_required()
    def put(self, car_id):
        args = car_parser.parse_args()
        car = Car.query.get(car_id)
        if car:
            car.make = args['make']
            car.model = args['model']
            car.year = args['year']
            db.session.commit()
            return {'id': car.id, 'make': car.make, 'model': car.model, 'year': car.year}
        return {'message': 'Автомобиль не найден'}, 404

    @jwt_required()
    def delete(self, car_id):
        car = Car.query.get(car_id)
        if car:
            db.session.delete(car)
            db.session.commit()
            return {'message': 'Автомобиль удалён'}
        return {'message': 'Автомобиль не найден'}, 404
