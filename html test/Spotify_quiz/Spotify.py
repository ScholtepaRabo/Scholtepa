import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sqlite3

# Set up Spotify API credentials
SPOTIPY_CLIENT_ID = '55a72fd6e0fb47e5906e08eea174df97'
SPOTIPY_CLIENT_SECRET = '8c25ff6abef94a10805f5f4e1ceff1a5'

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET
))

# Streamlit app
st.title('Spotify Song Search')

# Connect to SQLite database
conn = sqlite3.connect('spotify_songs.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS songs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        song_name TEXT,
        artist_name TEXT,
        spotify_url TEXT
    )
''')

# Function to add song to database
def add_song_to_db(user, song_name, artist_name, spotify_url):
    c.execute('SELECT COUNT(*) FROM songs WHERE user = ?', (user,))
    count = c.fetchone()[0]
    if count < 5:
        c.execute('INSERT INTO songs (user, song_name, artist_name, spotify_url) VALUES (?, ?, ?, ?)',
                    (user, song_name, artist_name, spotify_url))
        conn.commit()
        st.success('Song added to your database!')
    else:
        st.error('You can only add up to 5 songs.')

# User input for username
user = st.text_input('Enter your username')

if user:
    # Search box
    search_query = st.text_input('Enter song title')

    # Search button
    if st.button('Search'):
        if search_query:
            results = sp.search(q=search_query, type='track', limit=10)
            tracks = results['tracks']['items']
            if tracks:
                for idx, track in enumerate(tracks):
                    st.write(f"{idx+1}. {track['name']} by {', '.join([artist['name'] for artist in track['artists']])}")
                    st.write(f"[Listen on Spotify]({track['external_urls']['spotify']})")
                    if st.button(f'Add {track["name"]} to Database', key=idx):
                        song_name = track['name']
                        artist_name = ', '.join([artist['name'] for artist in track['artists']])
                        spotify_url = track['external_urls']['spotify']
                        add_song_to_db(user, song_name, artist_name, spotify_url)
            else:
                st.write("No results found.")

    # Display user's songs
    c.execute('SELECT song_name, artist_name, spotify_url FROM songs WHERE user = ?', (user,))
    user_songs = c.fetchall()
    if user_songs:
        st.write(f"### {user}'s Songs")
        for song_name, artist_name, spotify_url in user_songs:
            st.write(f"- [{song_name} by {artist_name}]({spotify_url})")
    else:
        st.write("No songs found for this user.")

# Display all songs in the database
st.write("### All Songs in Database")
c.execute('SELECT user, song_name, artist_name, spotify_url FROM songs')
all_songs = c.fetchall()
if all_songs:
    for user, song_name, artist_name, spotify_url in all_songs:
        st.write(f"- {user}: [{song_name} by {artist_name}]({spotify_url})")
else:
    st.write("No songs found in the database.")

# Close the connection at the end of the script
if conn:
    conn.close()
