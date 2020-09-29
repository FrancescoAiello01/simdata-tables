from flask import Flask
from flask_restful import Resource, Api
from flask import request, jsonify
from flask_cors import CORS
from utils import calculator_production

app = Flask(__name__) #create the Flask app
api = Api(app)
CORS(app)

@app.route('/')
def home():
    return '''<h1>SimData performance API home</h1>
            <p>This website calculates aircraft takeoff performance data for the Airbus A320</p>
            '''

@app.route('/calculate', methods=['POST']) #allow both GET and POST requests
def calculate():
    air_pressure = request.form.get('air_pressure')
    airport_elevation = request.form.get('airport_elevation')
    outside_air_temp = request.form.get('outside_air_temp')
    runway_length_uncorrected = request.form.get('runway_length_uncorrected')
    head_wind = request.form.get('head_wind')
    slope_percent = request.form.get('slope_percent')
    aircraft_weight = request.form.get('aircraft_weight')
    ap_registration = request.form.get('ap_registration')
    air_conditioning = request.form.get('air_conditioning')
    engine_anti_ice = request.form.get('engine_anti_ice')
    total_anti_ice = request.form.get('total_anti_ice')
    operational_CG_percentage =request.form.get('operational_CG_percentage')
    
    return '\n'.join(calculator_production.execute(air_pressure, airport_elevation, outside_air_temp, runway_length_uncorrected, head_wind, slope_percent, aircraft_weight, ap_registration, air_conditioning, engine_anti_ice, total_anti_ice, operational_CG_percentage))

if __name__ == '__main__':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000
