from flask import Flask, render_template, request, jsonify
import requests
import os
from prometheus_client import Counter, generate_latest

app = Flask(__name__)

REQUEST_COUNT = Counter('weather_app_requests_total', 'Total Weather App Requests', ['endpoint'])

RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY', '')

def get_weather_data(city):
    url = "https://weatherapi-com.p.rapidapi.com/current.json"
    querystring = {"q": city}
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "weatherapi-com.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            return response.json(), None
        return None, "City not found or API error."
    except Exception as e:
        return None, str(e)

@app.route('/', methods=['GET', 'POST'])
def home():
    REQUEST_COUNT.labels(endpoint='/').inc()
    weather_data = None
    error = None
    city = 'Cairo'  
    
    if request.method == 'POST':
        city = request.form.get('city', 'Cairo')
    
    weather_data, error = get_weather_data(city)
    return render_template('index.html', weather=weather_data, error=error, city=city)

@app.route('/weather', methods=['GET'])
def weather_api():
    REQUEST_COUNT.labels(endpoint='/weather').inc()
    city = request.args.get('city', 'Cairo')
    data, error = get_weather_data(city)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(data)

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)