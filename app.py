from flask import Flask, request, url_for, session, redirect, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth


#DEFINING CONSTS
CLIENT_ID = "77cd5595439347fab7eb244efd0f1f57"
CLIENT_SECRET = "f9f30355376645139c4100e74a860646"
TOKEN_INFO = "token_info"
SECRET_KEY = "PEANUTBUTTER"


#create authorization for user
def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=url_for("redirectPage", _external=True),
        scope="user-top-read user-library-read"
    )

#create flask app setup

app = Flask(__name__)

app.secret_key = SECRET_KEY

@app.route('/')
def index():
    name = 'username'
    return render_template('index.html', title='Welcome', username=name)



def get_token():
    token_info = session.get(TOKEN_INFO, None)
    return token_info


#build routes for pages

#craete 3 different tracklists render into html template
@app.route('/getTracks')
def getTracks():
    user_token = get_token()
    sp = spotipy.Spotify(
        auth=user_token['access_token']
    )
    short_term = sp.current_user_top_tracks(
        limit=10,
        offset=0,
        time_range="short_term"
    )
    medium_term = sp.current_user_top_tracks(
        limit=10,
        offset=0,
        time_range="medium_term"
    )
    long_term = sp.current_user_top_tracks(
        limit=10,
        offset=0,
        time_range="long_term"
    )

    return render_template('tracks.html',short_track=short_term['items'],med_track=medium_term['items'],long_track=long_term['items'])


#login page
@app.route('/login')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)



#redirect from login into track page using authorization access code from spotify api
@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear() 
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info    
    return redirect(url_for("getTracks", _external=True))

#stats of user
@app.route('/getStats')
def getStats():
    user_token = get_token()
    sp = spotipy.Spotify(auth=user_token['access_token'])

    # Fetch top artists
    top_artists = sp.current_user_top_artists(limit=5, time_range="long_term")

    # Fetch general listening stats (example: top track hours)
    top_tracks = sp.current_user_top_tracks(limit=50, time_range="long_term")

  

    return render_template(
        'stats.html',
        top_artists=top_artists['items'],
    )
    
if __name__ == '__main__':
    app.run(debug=True)