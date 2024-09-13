from flask import Flask, render_template, Response, request, redirect, session
import plotly.graph_objs as go
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, func
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash



from base64 import b64encode
from datetime import datetime


from Forms.LoginForm import LoginForm
from Forms.Registration import Registration
from Forms.user_forms.NewUserVehicle import NewUserVehicle
from Forms.admin_user_forms.UserEdit import UserEdit
from Forms.user_forms.UserSearch import UserSearch

app = Flask(__name__)
app.secret_key = 'key'

app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:kololokololo23@localhost/DB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    user_email = db.Column(db.String(20), primary_key=True)
    user_first_name = db.Column(db.String(20), nullable=False)
    user_second_name = db.Column(db.String(20), nullable=False)
    user_birthday = db.Column(db.Date, nullable=False)
    user_phone = db.Column(db.String(20), nullable=False)
    user_password = db.Column(db.String(20), nullable=False)
    vehicle_id_fk = db.relationship('Vehicle', secondary='association_user_vehicle')
    user_progress = db.relationship('Progress')
    

class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    vehicle_id = db.Column(db.Integer, primary_key=True)
    vehicle_brand = db.Column(db.String(50), nullable=False)
    vehicle_model = db.Column(db.String(50), nullable=False)
    vehicle_price = db.Column(db.Float, nullable=False)
    vehicle_year = db.Column(db.Date, nullable=True)
    kilowatt_hour = db.Column(db.Float, nullable=True)
    emissions_of_electricity = db.Column(db.Float, nullable=True)
    fuel_consumption = db.Column(db.Float, nullable=True)
    emission = db.Column(db.Float, nullable=True)
    fuel_type = db.Column(db.String(20), nullable=False)
    vehicle_title_image_name = db.Column(db.String, nullable=True)
    vehicle_title_image = db.Column(db.LargeBinary, nullable=False)
    vehicle_title_image_mimetype = db.Column(db.String, nullable=True)


class Association_User_Vehicle(db.Model):
    __tablename__ = 'association_user_vehicle'
    user_email = db.Column(db.String(20), db.ForeignKey('user.user_email'), primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.vehicle_id'), primary_key=True)


class Progress(db.Model):
    __tablename__ = 'progress'
    progress_id = db.Column(db.Integer, primary_key=True)
    emission_sum = db.Column(db.Float)
    fuel_sum = db.Column(db.Float)
    money_sum = db.Column(db.Float)
    user_email = db.Column(db.String(20), db.ForeignKey('user.user_email'))


class Comparison(db.Model):
    __tablename__ = 'comparison'
    comparison_id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(20), db.ForeignKey('user.user_email'), nullable=False)
    vehicle1_id = db.Column(db.Integer, db.ForeignKey('vehicle.vehicle_id'), nullable=False)
    vehicle2_id = db.Column(db.Integer, db.ForeignKey('vehicle.vehicle_id'), nullable=False)
    vehicle1_brand = db.Column(db.String(20), nullable=False)
    vehicle2_brand = db.Column(db.String(20), nullable=False)
    comparison_timestamp = db.Column(db.Date, nullable=False)

    user = db.relationship('User')
    vehicle1 = db.relationship('Vehicle', foreign_keys=[vehicle1_id])
    vehicle2 = db.relationship('Vehicle', foreign_keys=[vehicle2_id])


# create all tables
with app.app_context():
   db.create_all()
   try:
      db.session.query(Association_User_Vehicle).delete()
      db.session.query(Progress).delete()
      db.session.query(User).delete()
      db.session.query(Vehicle).delete()
      db.session.query(Comparison).delete()
      db.session.commit()
   except Exception as e:
      db.session.rollback()
      print(f"Error: {str(e)}")

# User
Kolya = User(user_email='kola@gmail.com',
           user_first_name='Kolya',
           user_second_name='Godnuy',
           user_phone='+399489384334',
           user_birthday='2003-4-21',
           user_password='qwerty123'
           )

# Progress
first_progress = Progress(
    emission_sum=0,
    fuel_sum=0,
    money_sum=0,
    user_email='kola@gmail.com',
)

# Auto

with open(r'@\\user\Downloads\main-page-slider-Porche.png', 'rb') as f:
    binary_data_of_imagePorche = f.read()


bmw_3_series = Vehicle(
    vehicle_brand='BMW',
    vehicle_model='M5',
    vehicle_price=2000.1212,
    vehicle_year='2024-03-7',

    fuel_consumption=10.1,
    emission=13.3,
    fuel_type='Benzin',
    kilowatt_hour=0,
    emissions_of_electricity=0,

    vehicle_title_image=binary_data_of_imagePorche,
    vehicle_title_image_name='gabriel-dias-pimenta-b6LZLf0IEm4-unsplash.jpg',
    vehicle_title_image_mimetype='image/jpeg',
)

bike = Vehicle(
    vehicle_brand='BIKE',
    vehicle_model='M54',
    vehicle_price=200,
    vehicle_year='2024-03-7',

    fuel_consumption=0,
    emission=0,
    fuel_type='Human-Powered',
    kilowatt_hour=0,
    emissions_of_electricity=0,

    vehicle_title_image=binary_data_of_imagePorche,
    vehicle_title_image_name='himiway-bikes-bx5brZFgSE8-unsplash.jpg',
    vehicle_title_image_mimetype='image/jpeg',
)

porche_911 = Vehicle(
    vehicle_brand='Porche',
    vehicle_model='911',
    vehicle_price=2000.1212,
    vehicle_year='2024-03-7',

    fuel_consumption=10.144,
    emission=22.3,
    fuel_type='Hybrid',
    kilowatt_hour=22,
    emissions_of_electricity=0,

    vehicle_title_image=binary_data_of_imagePorche,
    vehicle_title_image_name='porsche-911.jpg',
    vehicle_title_image_mimetype='image/jpeg',
)

mersides_s = Vehicle(
    vehicle_brand='Mersides',
    vehicle_model='S',
    vehicle_price=2000.1212,
    vehicle_year='2024-03-7',

    fuel_consumption=14.144,
    emission=22,
    fuel_type='Diesel',
    kilowatt_hour=0,
    emissions_of_electricity=0,
    
    vehicle_title_image=binary_data_of_imagePorche,
    vehicle_title_image_name='mercedes-benz-s-class-limousine-1.jpg',
    vehicle_title_image_mimetype='image/jpeg',
)

tesla = Vehicle(
    vehicle_brand='Tesla',
    vehicle_model='Model 3',
    vehicle_price=2000.1212,
    vehicle_year='2024-03-7',

    fuel_consumption=0,
    emission=0,
    fuel_type='Electric',
    kilowatt_hour=33,
    emissions_of_electricity=0,
    
    vehicle_title_image=binary_data_of_imagePorche,
    vehicle_title_image_name='tesla-5937063_1280.jpg',
    vehicle_title_image_mimetype='image/jpeg',
)

Kolya.user_progress.append(first_progress)

Kolya.vehicle_id_fk.append(bmw_3_series)

Kolya.vehicle_id_fk.append(porche_911)

Kolya.vehicle_id_fk.append(tesla)

Kolya.vehicle_id_fk.append(bike)

with app.app_context():
   db.session.add_all([
      Kolya, first_progress, 
      bmw_3_series, mersides_s, porche_911,
      tesla, bike,
   ])
   db.session.commit()

def newSession(email, pw):
    session['user_email'] = email
    session['role'] = 'user_email'
    
def dropSession():
    session['user_email'] = ''
    session['role'] = 'unlogged'


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            try:
                res = db.session.query(User).filter(User.user_email == form.user_email.data).one()
            except:
                form.user_email.errors = ['Користувача не знайдено']
                return render_template('login.html', form=form)
            if res.user_password == form.user_password.data:
                newSession(res.user_email, res.user_password)
                return redirect('/')
            else:
                form.user_password.errors = ['wrong password']
                return render_template('login.html', form=form)
        else:
            return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    dropSession()
    return redirect('/')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = Registration()
    if request.method == 'POST':
        if form.validate() and form.validate_birthday():
            try:
                new_user = User(
                    user_email=form.user_email.data,
                    user_first_name=form.user_first_name.data,
                    user_second_name=form.user_second_name.data,
                    user_phone=form.user_phone.data,
                    user_birthday=form.user_birthday.data,
                    user_password=form.user_password.data
                )
                db.session.add(new_user)
                db.session.commit()
                newSession(new_user.user_email, new_user.user_password)
                new_progress = Progress(
                    fuel_sum=0,
                    emission_sum=0,
                    money_sum=0,
                    user_email=session['user_email']
                )
                db.session.add(new_progress)
                db.session.commit()
                return render_template('index.html')
            except:
                form.user_email.errors = ['Цей користувач зареєстрований!']
                return render_template('registration.html', form=form)
        else:
            return render_template('registration.html', form=form)
    return render_template('registration.html', form=form)

@app.route('/', methods=['GET'])
def mainPage():
   all_vehicles = Vehicle.query.all()
   vehicles_json1 = []
   for vehicle in all_vehicles:
      vehicle_json = create_of_result_json_file(vehicle.vehicle_id)
      vehicles_json1.append(vehicle_json)
   return render_template('index.html', vehicles_json1=vehicles_json1)

@app.route('/user_page', methods=['GET'])
def user_page():
    result_user = db.session.query(User).filter(User.user_email == session['user_email']).one()
    return render_template('user/user_page.html', result_user=result_user)

@app.route('/user_change_data', methods=['GET'])
def user_change_data():
    result_user = db.session.query(User).filter(User.user_email == session['user_email']).one()

    return render_template('user_page/user_change_data.html', result_user=result_user)

@app.route('/user_change_vehicle', methods=['GET'])
def user_change_vehicle():
    vehicle_user_id = db.session.query(Association_User_Vehicle).filter(
        Association_User_Vehicle.user_email == session['user_email']).all()
    result_vehicle = []
    for vehicle_id in vehicle_user_id:
        result_vehicle.append(db.session.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id.vehicle_id).one())
    return render_template('user/user_vehicle.html', result_vehicle=result_vehicle)

@app.route('/delete_user_vehicle/<string:vehicle_id>', methods=['GET', 'POST'])
def delete_user_auto(vehicle_id):
    result = db.session.query(Association_User_Vehicle).filter(Association_User_Vehicle.vehicle_id == vehicle_id).one()
    db.session.delete(result)
    db.session.commit()
    return redirect('/user_change_vehicle')

@app.route('/user_vehicle_add', methods=['POST', 'GET'])
def user_vehicle_add():
    form = NewUserVehicle()

    latest_vehicle_id = db.session.query(Vehicle).order_by(Vehicle.vehicle_id.desc()).first()
    vehicle_last_id = latest_vehicle_id.vehicle_id + 1

    if request.method == 'POST':
        vehicle_image_blob = request.files['vehicle_title_image']
        vehicle_image_name = secure_filename(vehicle_image_blob.filename)
        vehicle_image_mimetype = vehicle_image_blob.mimetype

        if form.fuel_type.data == 'Electric':
            emission = 0
            kilowatt_hour = form.kilowatt_hour.data
            emissions_of_electricity = 0
            fuel_consumption = 0
        elif form.fuel_type.data == 'Diesel':
            emission = round(form.fuel_consumption.data * 0.274, 2)
            kilowatt_hour = 0
            emissions_of_electricity = 0
            fuel_consumption = form.fuel_consumption.data
        elif form.fuel_type.data == 'Benzin':
            emission = round(form.fuel_consumption.data * 0.239, 2)
            kilowatt_hour = 0
            emissions_of_electricity = 0
            fuel_consumption = form.fuel_consumption.data
        elif form.fuel_type.data == 'Hybrid':
            emission = round(form.fuel_consumption.data * 0.239, 2)
            kilowatt_hour = form.kilowatt_hour.data
            emissions_of_electricity = 0
            fuel_consumption = form.fuel_consumption.data
        else:
            emission = 0
            kilowatt_hour = 0
            emissions_of_electricity = 0
            fuel_consumption = 0
   
        new_vehicle = Vehicle(
            vehicle_id=vehicle_last_id,
            vehicle_brand=form.vehicle_brand.data,
            vehicle_model=form.vehicle_model.data,
            vehicle_price=form.vehicle_price.data,
            vehicle_year=form.vehicle_year.data,

            fuel_consumption=fuel_consumption,
            emission=emission,
            fuel_type=form.fuel_type.data,
            kilowatt_hour=kilowatt_hour,
            emissions_of_electricity=emissions_of_electricity,
            
            vehicle_title_image_name = vehicle_image_name,
            vehicle_title_image = vehicle_image_blob.read(),
            vehicle_title_image_mimetype = vehicle_image_mimetype,
        )
        db.session.add(new_vehicle)
        db.session.commit()

        new_association = Association_User_Vehicle(
            vehicle_id=vehicle_last_id,
            user_email=session['user_email']
        )
        db.session.add(new_association)
        db.session.commit()
        return redirect('/user_change_vehicle')
    elif request.method == 'GET':
        return render_template('user/user_vehicle_add.html', form=form)

@app.route('/vehicle_search', methods=['POST', 'GET'])
def vehicle_search():
    form = UserSearch()
    if request.method == 'POST':
        res_vehicle = db.session.query(Vehicle).filter(func.lower(Vehicle.vehicle_brand) == func.lower(form.search_value.data)).all()
        return render_template('user/user_search_data/vehicle_search_result.html', results_vehicle=res_vehicle)
    else:
        all_vehicles = Vehicle.query.all()
        vehicles_json = []
        for vehicle in all_vehicles:
         vehicle_json = create_of_result_json_file(vehicle.vehicle_id)
         vehicles_json.append(vehicle_json)
        return render_template('user/user_search_data/vehicle_search.html', form=form, vehicles_json=vehicles_json)

@app.route('/vehicle_search_result/<string:vehicle_id>', methods=['POST', 'GET'])
def add_vehicle_to_user(vehicle_id):
   association_exists = db.session.query(Association_User_Vehicle).filter_by(vehicle_id=vehicle_id, user_email=session['user_email']).first()

   error = 'Association already exists'

   if association_exists:
      return render_template('error.html', error=error), 409

   new_association = Association_User_Vehicle(
      vehicle_id=vehicle_id,
      user_email=session['user_email']
   )
   db.session.add(new_association)
   db.session.commit()
   vehicle_user_id = db.session.query(Association_User_Vehicle).filter(
   Association_User_Vehicle.user_email == session['user_email']).all()

   result_vehicle = []
   for vehicle_id in vehicle_user_id:
      result_vehicle.append(db.session.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id.vehicle_id).one())
   return '', 204

def get_vehicle_image(filename):
   img = Vehicle.query.filter(Vehicle.vehicle_title_image_name == filename).one()
   if not img:
      return 'Img not found', 404
   return img

def get_vehicle_by_id(vehicle_id):
   vehicle = Vehicle.query.get(vehicle_id)
   return vehicle

def get_user_first_second_name(vehicle_id):
   user = (db.session.query(User.user_first_name,
                           User.user_second_name)
            .join(Vehicle, Vehicle.user_id == User.user_id)
            .filter(Vehicle.vehicle_id == vehicle_id)).one()

   user_first_name = user.user_first_name
   user_second_name = user.user_second_name
   return user_first_name, user_second_name

def create_of_result_json_file(vehicle_id):
   result_vehicle_content = get_vehicle_by_id(vehicle_id)
   vehicle_title_image = b64encode(result_vehicle_content.vehicle_title_image).decode('utf-8')
   result_json = {
      'vehicle_brand': result_vehicle_content.vehicle_brand,
      'vehicle_model': result_vehicle_content.vehicle_model,
      'vehicle_price': result_vehicle_content.vehicle_price,
      'vehicle_year': result_vehicle_content.vehicle_year,

      'fuel_consumption': result_vehicle_content.fuel_consumption,
      'emission': result_vehicle_content.emission,
      'fuel_type': result_vehicle_content.fuel_type,
      'kilowatt_hour': result_vehicle_content.kilowatt_hour,
      'emissions_of_electricity': result_vehicle_content.emissions_of_electricity,

      'vehicle_title_image': vehicle_title_image,
      'vehicle_title_image_name': result_vehicle_content.vehicle_title_image_name,
      'vehicle_title_image_mimetype': result_vehicle_content.vehicle_title_image_mimetype,
   }
   return result_json

@app.route("/user_vehicle_add/image/<string:filename>")
def vehicle_image(filename):
    img = get_vehicle_image(filename)
    return Response(img.vehicle_title_image, mimetype=img.vehicle_title_image_mimetype)

@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def vehicle_content(vehicle_id):
   result_json = create_of_result_json_file(vehicle_id)

   return render_template('user/open_vehicle.html',
                        result_json=result_json,
                        # user_first_name=user_first_name,
                        # user_last_name=user_second_name
                        )

@app.route('/edit_user/<string:email>', methods=['GET', 'POST'])
def edit_user(email):
    form = UserEdit()
    result = db.session.query(User).filter(User.user_email == email).one()
    if request.method == 'GET':
        form.user_first_name.data = result.user_first_name
        form.user_second_name.data = result.user_second_name
        form.user_email.data = result.user_email
        form.user_birthday.data = result.user_birthday
        form.user_phone.data = result.user_phone
        return render_template('user/edit_user.html', form=form, form_name=email)
    elif request.method == 'POST':
        if form.validate() and form.validate_birthday():
            result.user_first_name = form.user_first_name.data
            result.user_second_name = form.user_second_name.data
            result.user_email = form.user_email.data
            result.user_birthday = form.user_birthday.data,
            result.user_phone = form.user_phone.data
            db.session.commit()
            return redirect('/user_page')
        else:
            if not form.validate_birthday():
                form.user_birthday.errors = ['Має бути > 1900']
            return render_template('user/edit_user.html', form=form)

@app.route('/user_progress', methods=['GET'])
def user_progress():
    result_progress = db.session.query(Progress).filter(Progress.user_email == session['user_email']).one()
    return render_template('user/user_progress.html', result_progress=result_progress)

@app.route('/user_comparessions', methods=['GET'])
def user_comparession():
    result_comparessions = db.session.query(Comparison).filter(Comparison.user_email == session['user_email']).all()
    
    return render_template('user/user__comparession.html', result_comparessions=result_comparessions)

@app.route('/compare', methods=['GET', 'POST'])
def compare():
    if request.method == 'POST':
        vehicle1_id = request.form.get('vehicle1')
        vehicle2_id = request.form.get('vehicle2')
        vehicle1 = Vehicle.query.get(vehicle1_id)
        vehicle2 = Vehicle.query.get(vehicle2_id)
        comparison_timestamp = datetime.now()
        environment_impact_1 = calculate_environmental_impact(vehicle1)
        environment_impact_2 = calculate_environmental_impact(vehicle2)
        result1_json = create_of_result_json_file(vehicle1_id)
        result2_json = create_of_result_json_file(vehicle2_id)
        comparison = Comparison(
            user_email=session['user_email'],
            vehicle1_id=vehicle1_id,
            vehicle2_id=vehicle2_id,
            vehicle1_brand=vehicle1.vehicle_brand,
            vehicle2_brand=vehicle2.vehicle_brand,
            comparison_timestamp=comparison_timestamp
        )
        db.session.add(comparison)
        db.session.commit()
        plot1_div = create_comparison_of_price_plot(vehicle1, vehicle2)
        plot2_div = create_comparison_of_еmission_plot(vehicle1, vehicle2)
        plot3_div = create_comparison_of_fuel_consumption_plot(vehicle1, vehicle2)
        return render_template('user/compare.html', result1_json=result1_json, result2_json=result2_json, 
                               plot1_div=plot1_div, plot2_div=plot2_div, plot3_div=plot3_div,
                               environment_impact_1=environment_impact_1, environment_impact_2=environment_impact_2)
    vehicle_user_id = db.session.query(Association_User_Vehicle).filter(
      Association_User_Vehicle.user_email == session['user_email']).all()
    vehicles = Vehicle.query.all()
    result_vehicle = []
    for vehicle_id in vehicle_user_id:
        result_vehicle.append(db.session.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id.vehicle_id).one())
    return render_template('user/vehicle_compare.html', result_vehicle=result_vehicle, vehicles=vehicles)

def create_comparison_of_price_plot(vehicle1, vehicle2):
    categories = [
        'Ціна (грн)'
        ]
    values_vehicle1 = [
        vehicle1.vehicle_price
        ]
    values_vehicle2 = [
        vehicle2.vehicle_price
        ]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=categories, y=values_vehicle1, name=vehicle1.vehicle_brand))
    fig.add_trace(go.Bar(x=categories, y=values_vehicle2, name=vehicle2.vehicle_brand))
    fig.update_layout(barmode='group', title='Порівняння між транспортними засобами', xaxis_title='Категорія', yaxis_title='Значення (грн)')
    plot_div = fig.to_html(full_html=False)
    return plot_div

def create_comparison_of_еmission_plot(vehicle1, vehicle2):
   categories = []
   if vehicle1.fuel_type == 'Electric':
      values_vehicle1 = [0, vehicle1.emissions_of_electricity]
      categories.append('Викиди від електроенергії')
   elif vehicle1.fuel_type == 'Hybrid':
      values_vehicle1 = [vehicle1.emission, vehicle1.emissions_of_electricity]
      categories.append('Викиди від електроенергії')
   else:
      values_vehicle1 = [vehicle1.emission, 0]
      categories.append('Викиди двигуна (CO2)')
   if vehicle2.fuel_type == 'Electric':
      values_vehicle2 = [0, vehicle2.emissions_of_electricity]
      categories.append('Викиди від електроенергії')
   elif vehicle2.fuel_type == 'Hybrid':
      values_vehicle2 = [vehicle2.emission, vehicle2.emissions_of_electricity]
      categories.append('Викиди від електроенергії')
   else:
      values_vehicle2 = [vehicle2.emission, 0]
      categories.append('Викиди двигуна (CO2)')
   fig = go.Figure()
   fig.add_trace(go.Bar(x=categories, y=values_vehicle1, name=vehicle1.vehicle_brand))
   fig.add_trace(go.Bar(x=categories, y=values_vehicle2, name=vehicle2.vehicle_brand))
   fig.update_layout(barmode='group', 
                     title='Порівняння між транспортними засобами', 
                     xaxis_title='Категорія', 
                     yaxis_title='Викиди CO2(кг/100 км)')
   plot_div = fig.to_html(full_html=False)
   return plot_div
    
def create_comparison_of_fuel_consumption_plot(vehicle1, vehicle2):
    categories = []
    if vehicle1.fuel_type == 'Electric':
      values_vehicle1 = [0, vehicle1.kilowatt_hour]
      categories.append('Споживання електроенергії (кіловат/год)')
    elif vehicle1.fuel_type == 'Hybrid':
      values_vehicle1 = [vehicle1.fuel_consumption, vehicle1.kilowatt_hour]
      categories.append('Споживання електроенергії (кіловат/год)')
    else:
         values_vehicle1 = [vehicle1.fuel_consumption, 0]
         categories.append('Витрата палива (л/км)')
    if vehicle2.fuel_type == 'Electric':
      values_vehicle2 = [0, vehicle2.kilowatt_hour]
      categories.append('Споживання електроенергії (кіловат/год)')
    elif vehicle2.fuel_type == 'Hybrid':
      values_vehicle2 = [vehicle2.fuel_consumption, vehicle2.kilowatt_hour]
      categories.append('Споживання електроенергії (кіловат/год)')
    else:
      values_vehicle2 = [vehicle2.fuel_consumption, 0]
      categories.append('Витрата палива (л/км)')
    fig = go.Figure()
    fig.add_trace(go.Bar(x=categories, y=values_vehicle1, name=vehicle1.vehicle_brand))
    fig.add_trace(go.Bar(x=categories, y=values_vehicle2, name=vehicle2.vehicle_brand))
    fig.update_layout(barmode='group', title='Порівняння між транспортними засобами', xaxis_title='Категорія', yaxis_title='Витрата палива')
    plot_div = fig.to_html(full_html=False)

    return plot_div

def calculate_environmental_impact(vehicle):
    environmental_impact = 0
    if vehicle.fuel_type == 'Benzin':
        environmental_impact += vehicle.emission
    elif vehicle.fuel_type == 'Diesel':
        environmental_impact += vehicle.emission
    elif vehicle.fuel_type == 'Electric':
        environmental_impact += vehicle.emissions_of_electricity
    elif vehicle.fuel_type == 'Hybrid':
        environmental_impact += vehicle.emission
    elif vehicle.fuel_type == 'Human-powered':
        environmental_impact = 0
    return environmental_impact

@app.route('/route', methods=['GET'])
def user_main_page():
    result_progress = db.session.query(Progress).filter(Progress.user_email == session['user_email']).one()
    vehicle_user_id = db.session.query(Association_User_Vehicle).filter(
        Association_User_Vehicle.user_email == session['user_email']).all()

    result_vehicle = []
    for vehicle_id in vehicle_user_id:
        result_vehicle.append(db.session.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id.vehicle_id).one())

    return render_template('user/route.html', result_progress=result_progress, result_vehicle=result_vehicle)

@app.route('/get_distance', methods=['GET', 'POST'])
def get_distance():
    global distance
    if request.method == 'POST':
        distance = request.get_json()["distance"].split(" ")[0].replace(",", ".")
        return 'OK', 200

@app.route('/add_progress/<string:vehicle_id>', methods=['GET', 'POST'])
def add_progress(vehicle_id):
    selectedVeh = db.session.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).one()

    priceOfFuel = request.get_json()["priceFuel"]
    
    fuel_sum = "{:.2f}".format((float(selectedVeh.fuel_consumption) / 100) * float(distance))
    money_sum = "{:.2f}".format(float(fuel_sum) * float(priceOfFuel), 2)
    emission_sum = "{:.2f}".format((float(selectedVeh.emission) / 100) * float(distance))

    progres_value = db.session.query(Progress).filter(Progress.user_email == session['user_email']).one()

    progres_value.emission_sum += float(emission_sum)
    progres_value.fuel_sum += float(fuel_sum)
    progres_value.money_sum += float(money_sum)

    progres_value.emission_sum = float(progres_value.emission_sum)
    progres_value.fuel_sum = float(progres_value.fuel_sum)
    progres_value.money_sum = float(progres_value.money_sum)

    db.session.commit()
    return 'good!', 200


if __name__ == '__main__':
    app.run(debug=True)