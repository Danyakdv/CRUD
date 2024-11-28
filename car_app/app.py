from flask import Flask, render_template, redirect, url_for, flash, jsonify, request
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_swagger_ui import get_swaggerui_blueprint
from models import db, User, Car
from forms import RegistrationForm, LoginForm, CarForm
from resources import CarResource

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)
jwt = JWTManager(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

api = Api(app)
api.add_resource(CarResource, '/api/cars', '/api/cars/<int:car_id>')

SWAGGER_URL = '/api/docs'  
API_URL = '/static/swagger.json'  

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Car App API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация прошла успешно. Пожалуйста, войдите.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            access_token = create_access_token(identity=user.id)
            response = jsonify({'access_token': access_token})
            response.set_cookie('token', access_token)
            flash('Вход выполнен успешно.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неверное имя пользователя или пароль.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('index'))

@app.route('/cars', methods=['GET', 'POST'])
@login_required
def car_list():
    form = CarForm()
    if form.validate_on_submit():
        new_car = Car(make=form.make.data, model=form.model.data, year=form.year.data, user_id=current_user.id)
        db.session.add(new_car)
        db.session.commit()
        flash('Автомобиль успешно добавлен.', 'success')
        return redirect(url_for('car_list'))
    cars = Car.query.filter_by(user_id=current_user.id).all()
    return render_template('car_list.html', cars=cars, form=form)

@app.route('/cars/<int:car_id>/edit', methods=['GET', 'POST'])
@login_required
def car_edit(car_id):
    car = Car.query.get_or_404(car_id)
    if car.user_id != current_user.id:
        flash('У вас нет прав для редактирования этого автомобиля.', 'danger')
        return redirect(url_for('car_list'))
    form = CarForm(obj=car)
    if form.validate_on_submit():
        form.populate_obj(car)
        db.session.commit()
        flash('Автомобиль успешно обновлен.', 'success')
        return redirect(url_for('car_list'))
    return render_template('car_form.html', form=form, car=car)

@app.route('/cars/<int:car_id>/delete', methods=['POST'])
@login_required
def car_delete(car_id):
    car = Car.query.get_or_404(car_id)
    if car.user_id != current_user.id:
        flash('У вас нет прав для удаления этого автомобиля.', 'danger')
        return redirect(url_for('car_list'))
    db.session.delete(car)
    db.session.commit()
    flash('Автомобиль успешно удален.', 'success')
    return redirect(url_for('car_list'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)

