from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route("/")
def index():
    # Fetch data from the API
    response = requests.get('http://smashdb.me/api/character/')
    if response.status_code != 200:
        return f"Error: Unable to fetch character data (status code {response.status_code})", 500

    data = response.json()
    character_list = data.get('results', [])

    characters = []

    for character in character_list:
        url = character.get('url', '')
        parts = url.split("/")
        id = parts[-1] if parts else 'Unknown'

        # Build an image URL using the ID
        image_url = f"http://smashdb.me/api/character/{id}/image"

        characters.append({
            'name': character.get('name', 'Unknown').capitalize(),
            'id': id,
            'image_url': image_url
        })

    # Render the template with the fetched data
    return render_template('index.html', characters=characters)

@app.route("/character/<int:id>")
def character_detail(id):
    # Fetch data from the API
    response = requests.get(f'http://smashdb.me/api/character/{id}')
    if response.status_code != 200:
        return f"Error: Unable to fetch character data (status code {response.status_code})", 500

    data = response.json()

    weight = data.get('weight', 'Unknown')
    moves = data.get('moves', [])
    universe = data.get('universe', 'Unknown')
    name = data.get('name', 'Unknown').capitalize()
    image_url = f"http://smashdb.me/api/character/{id}/image"

    # Render the template with the fetched data
    return render_template('character.html', character={
        'name': name,
        'id': id,
        'image': image_url,
        'weight': weight,
        'moves': moves,
        'universe': universe,
    })

if __name__ == '__main__':
    app.run(debug=True)