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





@app.route("/playlist", methods=["GET"])
def playlist_get():
    playlist_list = list(db.playlist.find({}, {'_id': False}))
    return jsonify({'playlist': playlist_list})



@app.route("/playlist", methods=["POST"])
def search_track():
    track_input_receive = request.form.get('track_input')

    track_count = db.playlist.find_one({"track": track_input_receive})

    if track_count:
        db.playlist.update_one({"_id": track_count["_id"]}, {"$inc": {"count": 1}})
        message = f"'{track_input_receive}'은 이미 모아졌어요."
    else:
        db.playlist.insert_one({"track": track_input_receive, "count": 1})
        message = f"'{track_input_receive}'가 모아졌어요!"

    return message

def playlist_post():
    track_input_receive = request.form['track_input']
    date = request.form['date_input']
    likes = request.form['like']


    track_results = []
    artists_results = []

    track_search = sp.search(track_input_receive, limit=10, type='track', market=None)

    for track in track_search['tracks']['items']:

        for artist in track['artists']:
            artists_result = artist['name']
            artists_results.append(artists_result)

        track_result = track['name']
        track_results.append(track_result)


    return jsonify({'msg': '비빔밥에 추가되었어요'})


    doc = {
        'track': track_results,
        'artists': artists_results,
        'image': image,
        'date': date,
        'likes': likes,
        'count': count

    }
    db.playlist.insert_one(doc)




if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
