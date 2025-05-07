from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get the API key from the .env file
WEATHER_API_KEY = os.getenv('API_KEY')

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error = None

    if request.method == 'POST':
        location = request.form.get('location')

        if location:
            # Make a request to the WeatherAPI
            url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={location}"
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise an error for HTTP issues
                weather_data = response.json()
            except requests.RequestException as e:
                error = f"Error fetching weather data: {e}"

    return render_template('index.html', weather_data=weather_data, error=error)

if __name__ == '__main__':
    app.run(debug=True)