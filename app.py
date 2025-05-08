from flask import Flask, render_template, request, redirect, url_for, session
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session

WEATHER_API_KEY = os.getenv('API_KEY')

# --------------------------
# Reusable Weather Function
# --------------------------
def fetch_weather(location):
    try:
        url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={location}&days=1"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {'error': str(e)}

# --------------------------
# Homepage Route
# --------------------------
@app.route('/')
def index():
    error = session.pop('error', None)
    return render_template('index.html', error=error)

# --------------------------
# Handle Form Submission
# --------------------------
@app.route('/weather', methods=['POST'])
def redirect_to_city():
    location = request.form.get('location')
    if location:
        return redirect(url_for('weather_by_city', city=location))
    else:
        session['error'] = "Please enter a valid location."
        return redirect(url_for('index'))

# --------------------------
# Dynamic URL: Show weather
# --------------------------
@app.route('/weather/<city>')
def weather_by_city(city):
    data = fetch_weather(city)
    
    if 'error' in data:
        return render_template('error.html', message=data['error']), 400

    # Filter forecast: only show warm hours
    warm_hours = [
        hour for hour in data['forecast']['forecastday'][0]['hour']
        if hour['temp_c'] > 20
    ]

    return render_template(
        'weather.html',
        weather_data=data,
        warm_hours=warm_hours
    )

# --------------------------
# Error Page Route (Optional)
# --------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', message="Page not found."), 404

if __name__ == '__main__':
    app.run(debug=True)