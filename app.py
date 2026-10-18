import os
import time
from flask import Flask, jsonify, request
import requests
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# إعداد Prometheus Metrics للمراقبة
REQUEST_COUNT = Counter(
    'app_request_total', 'Total Request Count', ['method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram(
    'app_request_latency_seconds', 'Request latency', ['endpoint']
)

# بيانات RapidAPI (يفضل لاحقاً نتحكم فيها عبر Environment Variables)
RAPIDAPI_KEY = os.environ.get('RAPIDAPI_KEY', 'YOUR_RAPIDAPI_KEY_HERE')
RAPIDAPI_HOST = os.environ.get('RAPIDAPI_HOST', 'weatherapi-com.p.rapidapi.com')

@app.route('/weather', methods=['GET'])
def get_weather():
    start_time = time.time()
    city = request.args.get('city', 'Cairo')
    
    url = f"https://{RAPIDAPI_HOST}/current.json"
    querystring = {"q": city}
    
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        status_code = response.status_code
        
        # تسجيل الـ Metrics
        resp_time = time.time() - start_time
        REQUEST_LATENCY.labels(endpoint='/weather').observe(resp_time)
        REQUEST_COUNT.labels(method='GET', endpoint='/weather', http_status=status_code).inc()
        
        if status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": "Failed to fetch data from RapidAPI", "details": response.text}), status_code
            
    except Exception as e:
        REQUEST_COUNT.labels(method='GET', endpoint='/weather', http_status=500).inc()
        return jsonify({"error": str(e)}), 500

# Endpoint مخصص عشان Prometheus يقدر يقرا المتركس منه
@app.route('/metrics', methods=['GET'])
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)