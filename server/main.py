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
            <p>Click <a href="/calculate">here</a> to access the calculator</p>'''

@app.route('/calculate', methods=['GET', 'POST']) #allow both GET and POST requests
def calculate():
    if request.method == 'POST': #this block is only entered when the form is submitted
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

    return '''<form method="POST">
                  air_pressure: <input type="text" name="air_pressure"><br>
                  airport_elevation: <input type="text" name="airport_elevation"><br>
                  outside_air_temp: <input type="text" name="outside_air_temp"><br>
                  runway_length_uncorrected: <input type="text" name="runway_length_uncorrected"><br>
                  head_wind: <input type="text" name="head_wind"><br>
                  slope_percent: <input type="text" name="slope_percent"><br>
                  aircraft_weight: <input type="text" name="aircraft_weight"><br>
                  ap_registration: <input type="text" name="ap_registration"><br>
                  air_conditioning: <input type="text" name="air_conditioning"><br>
                  engine_anti_ice: <input type="text" name="engine_anti_ice"><br>
                  total_anti_ice: <input type="text" name="total_anti_ice"><br>
                  operational_CG_percentage: <input type="text" name="operational_CG_percentage"><br>
                  <input type="submit" value="Submit"><br>
              </form>
              <p> Example input: </p>
              <p>air_pressure 990</p><p>airport_elevation 1000</p><p>outside_air_temp 35</p><p>runway_length_uncorrected 2750</p><p>head_wind 10</p><p>slope_percent 1</p><p>aircraft_weight 66</p><p>AP_registration False</p><p>air_conditioning False</p><p>engine_anti_ice True</p><p>total_anti_ice False</p><p>operational_CG_percentage 26 </p>
              '''

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

if __name__ == '__main__':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000
