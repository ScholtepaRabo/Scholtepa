import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize or load existing DataFrame
@st.cache_data
def load_data():
    try:
        return pd.read_csv('spotify_top5.csv')
    except FileNotFoundError:
        return pd.DataFrame(columns=['timestamp', 'user_name', 'song1', 'artist1', 
                                   'song2', 'artist2', 'song3', 'artist3', 
                                   'song4', 'artist4', 'song5', 'artist5'])

# Set up the Streamlit page
st.title('My Spotify Top 5 Songs')
st.write('Share your current favorite songs!')

# Load the existing data
df = load_data()

# Create the input form
with st.form('spotify_form'):
    user_name = st.text_input('Your Name')
    
    # Create 5 pairs of input fields for songs and artists
    songs_data = {}
    for i in range(1, 6):
        col1, col2 = st.columns(2)
        with col1:
            songs_data[f'song{i}'] = st.text_input(f'Song #{i}')
        with col2:
            songs_data[f'artist{i}'] = st.text_input(f'Artist #{i}')
    
    submitted = st.form_submit_button('Submit')
    
    if submitted:
        if user_name and all(songs_data.values()):
            # Prepare new data entry
            new_data = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'user_name': user_name,
                **songs_data
            }
            
            # Add new data to DataFrame
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            
            # Save updated DataFrame
            pd.DataFrame([new_data]).to_csv('spotify_top5.csv', 
                mode='a', 
                header=not pd.io.common.file_exists('spotify_top5.csv'), 
                index=False)
            
            st.success('Your top 5 has been saved!')
            
            # Clear the cache to show the updated data
            load_data.clear()
        else:
            st.error('Please fill in all fields!')
