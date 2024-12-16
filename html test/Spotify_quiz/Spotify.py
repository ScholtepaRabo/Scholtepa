import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sqlite3

# Set up Spotify API credentials
SPOTIPY_CLIENT_ID = 'xx'
SPOTIPY_CLIENT_SECRET = 'xx'

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET
))

# Streamlit app
st.title('Spotify Song Search')

# Connect to SQLite database
try:
    conn = sqlite3.connect('spotify_songs.db')
    c = conn.cursor()
    st.success("Successfully connected to database")
except sqlite3.Error as e:
    st.error(f"Error connecting to database: {e}")
    exit(1)

# Create tables if they don't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS songs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        song_name TEXT,
        artist_name TEXT,
        spotify_url TEXT
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE
    )
''')

# Insert users into the users table
users = ['Rene', 'Sandra', 'Duco', 'Anne']
for user in users:
    c.execute('INSERT OR IGNORE INTO users (username) VALUES (?)', (user,))
conn.commit()

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
    # Check if the user is registered
    c.execute('SELECT COUNT(*) FROM users WHERE username = ?', (user,))
    if c.fetchone()[0] == 0:
        st.error('User not registered.')
    else:
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
try:
    c.execute('SELECT user, song_name, artist_name, spotify_url FROM songs')
    all_songs = c.fetchall()
    if all_songs:
        for user, song_name, artist_name, spotify_url in all_songs:
            st.write(f"- {user}: [{song_name} by {artist_name}]({spotify_url})")
    else:
        st.write("No songs found in the database.")
finally:
    # Close the connection at the end of the script
    if conn:
        conn.close()
