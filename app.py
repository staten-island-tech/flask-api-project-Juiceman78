from flask import Flask, render_template 
import requests 

app = Flask(__name__)

@app.route('/')
def index():

    # Fetch data from the API
    response = requests.get('http://smashdb.me/api/character/')
    data = response.json()
    character_list= data['results']

    characters = []

    for character in character_list:

        url = character['url']
        

    # Render the template with the fetched data
    return render_template('index.html', data=data)