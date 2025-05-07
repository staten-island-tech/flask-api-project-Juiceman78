from flask import Flask, render_template, request, redirect, url_for, session
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for using session

# Get the API key from the .env file
WEATHER_API_KEY = os.getenv('API_KEY')

@app.route('/', methods=['GET'])
def index():
    # Display the form only
    error = session.pop('error', None)  # Get and remove error if it exists
    return render_template('index.html', error=error)

@app.route('/weather', methods=['POST', 'GET'])
def weather():
    if request.method == 'POST':
        location = request.form.get('location')

        if location:
            # Make a request to WeatherAPI
            url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={location}"
            try:
                response = requests.get(url)
                response.raise_for_status()
                weather_data = response.json()
                session['weather_data'] = weather_data
                return redirect(url_for('weather'))  # GET method to display results
            except requests.RequestException as e:
                session['error'] = f"Error fetching weather data: {e}"
                return redirect(url_for('index'))
        else:
            session['error'] = "Please enter a location."
            return redirect(url_for('index'))

    # GET request — show the weather result page
    weather_data = session.get('weather_data')
    if not weather_data:
        return redirect(url_for('index'))  # No data? Redirect back

    return render_template('weather.html', weather_data=weather_data)

if __name__ == '__main__':
    app.run(debug=True)