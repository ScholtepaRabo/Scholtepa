import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# Set your Spotify API credentials
SPOTIPY_CLIENT_ID = 'xx'
SPOTIPY_CLIENT_SECRET = 'xx'

# Initialize Spotify client
client_credentials_manager = SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID, 
    client_secret=SPOTIPY_CLIENT_SECRET
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def search_spotify(query):
    results = sp.search(q=query, limit=5, type='track')
    return results['tracks']['items']

# Set page title
st.title("Spotify Top 5 Songs App")

# Create name input form
with st.form("name_form"):
    name = st.text_input("Please enter your name:")
    submit_name = st.form_submit_button("Submit")

if submit_name and name:
    st.write(f"Hello, {name}!")

# Initialize an empty data frame to store the results
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=['Username', 'Title', 'Artist', 'Spotify URL'])

# Create search form
if name:
    with st.form("search_form"):
        search_query = st.text_input("Search for a song or artist:")
        submit_search = st.form_submit_button("Search")
    
    if submit_search and search_query:
        st.subheader("Search Results:")
        results = search_spotify(search_query)
        
        if results:
            for idx, track in enumerate(results, 1):
                st.write(f"{idx}. {track['name']} - {track['artists'][0]['name']}")
                # Display album cover
                if track['album']['images']:
                    st.image(track['album']['images'][0]['url'], width=100)
                # Add a preview URL if available
                if track['preview_url']:
                    st.audio(track['preview_url'])
                
                # Add a button to store the result in the data frame and write to CSV
                if st.button(f"Save {track['name']}", key=f"save_{idx}"):
                    new_row = {
                        'Username': name,
                        'Title': track['name'],
                        'Artist': track['artists'][0]['name'],
                        'Spotify URL': track['external_urls']['spotify']
                    }
                    st.session_state.df = st.session_state.df.append(new_row, ignore_index=True)
                    st.session_state.df.to_csv('saved_songs.csv', index=False)
                    st.write("Saved and written to CSV!")
                st.write("---")
        else:
            st.write("No results found.")

# Display the data frame
if not st.session_state.df.empty:
    st.subheader("Saved Songs")
    st.dataframe(st.session_state.df)

# Add some styling
st.markdown("""
    <style>
    .stButton button {
        background-color: #1DB954;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
