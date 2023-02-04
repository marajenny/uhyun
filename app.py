import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient(
    'mongodb+srv://spartsyl:U6V10Jk7juI7SMEX@Cluster0.fsdg43e.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.Bibimbap

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

cid = 'aa4b6b300fdb4797bfe7625e121c99cd'
secret = 'ddbca51759f340e58471ec1b929bad7b'


client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)



@app.route('/')
def home():
    return render_template('index.html')


@app.route("/search_results", methods=["POST"])
def search_results():
    track_input_receive = request.form.get('track_input')

    track_search = sp.search("attention", limit=10, type='track', market=None)

    track_results = []
    artists_results = []
    image_results = []

    for track in track_search['tracks']['items']:

        for artist in track['artists']:
            artists_result = artist['name']
            artists_results.append(artists_result)

        album = track['album']
        for image in album['images']:
            image_result = image['url']
            image_results.append(image_result)

        track_result = track['name']
        track_results.append(track_result)

    print(track_results[0])
    print(artists_results[0])
    print(image_results[0])

    print(track_results[1])
    print(artists_results[1])
    print(image_results[1])

    doc = {
        'track': track_results,
        'artists': artists_results,
        'image' : image_results,

    }
    db.search_results.insert(doc)


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