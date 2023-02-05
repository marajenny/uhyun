import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient(
    'mongodb+srv://spartsyl:U6V10Jk7juI7SMEX@Cluster0.fsdg43e.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.Bibimbap

cid = 'aa4b6b300fdb4797bfe7625e121c99cd'
secret = 'ddbca51759f340e58471ec1b929bad7b'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)




@app.route('/')
def home():
    return render_template('index.html')


@app.route("/search_results", methods=["POST"])
def search_results():
    track_input_receive = request.form['track_input']
    track_search = sp.search(track_input_receive, limit=10, type='track', market=None)

    tracks = []

    for track in track_search['tracks']['items']:
        track_results = track['name']
        artist_results = [artist['name'] for artist in track['artists']]
        image_results = next(
            (image['url'] for image in track['album']['images'] if image['height'] == 640 and image['width'] == 640),
            None)
        url_results = track['preview_url']

        date_input = datetime.now().date()
        hour_input = datetime.now().time()

        track_result = {
            'track': track_results,
            'artists': artist_results,
            'image': image_results,
            'url': url_results,
            'date': date_input.strftime('%Y-%m-%d'),
            'hour': str(hour_input)[:2]}
        tracks.append(track_result)

        db.search_results.insert_one(track_result)


@app.route("/playlists", methods=["POST"])
def selected_title():


    date_input_receive = request.form['date_input']
    hour_input_receive = request.form['hour_input']
    count = db.playlist.count()


    doc = {
        'track': track_selected,
        'artists': artists_selected,
        'date': date_input_receive,
        'hour': hour_input_receive,
        'count': count,

    }
    db.playlist.insert_one(doc)


@app.route("/playlist", methods=["GET"])
def playlist_get():
    playlist_list = list(db.playlist.find({}, {'_id': False}))
    return jsonify({'playlist': playlist_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)