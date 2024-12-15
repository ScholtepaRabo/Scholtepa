from email.mime.text import MIMEText
import streamlit as st
import sqlite3
import smtplib
import secrets

# Initialize database
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, 
                  email TEXT UNIQUE,
                  dob DATE,
                  birthplace TEXT,
                  verified BOOLEAN,
                  verification_token TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS spotify_songs
                 (username TEXT,
                  song_name TEXT,
                  artist TEXT,
                  rank INTEGER,
                  FOREIGN KEY(username) REFERENCES users(username))''')
    conn.commit()
    conn.close()

# Send verification email
def send_verification_email(email, token):
    # Configure your email settings here
    sender_email = "scholtepa@hotmail.com"  # Replace with your email
    smtp_password = "Dwn7S*ag5U5&"      # Replace with your app password
    
    msg = MIMEText(f"Click here to verify your account: http://localhost:8501/verify?token={token}")
    msg['Subject'] = "Verify your Xmas Quiz registration"
    msg['From'] = sender_email
    msg['To'] = email

    try:
        s = smtplib.SMTP('smtp-mail.outlook.com', 587)
        s.starttls()
        s.login(sender_email, smtp_password)
        s.sendmail(sender_email, [email], msg.as_string())
        s.quit()
    except Exception as e:
        st.error(f"Failed to send email: {str(e)}")

# Register user
def register_user(username, email, dob, birthplace):
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        token = secrets.token_urlsafe(16)
        c.execute('INSERT INTO users (username, email, dob, birthplace, verified, verification_token) VALUES (?, ?, ?, ?, 0, ?)', (username, email, dob, birthplace, token))
        conn.commit()
        conn.close()
        send_verification_email(email, token)
    except sqlite3.IntegrityError:
        st.error('Username or email already exists')
    except Exception as e:
        st.error(f'An error occurred: {str(e)}')

# Verify user
def verify_user(token):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('UPDATE users SET verified = 1 WHERE verification_token = ?', (token,))
    conn.commit()
    conn.close()

# Add song to database
def add_song(username, song_name, artist, rank):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('INSERT INTO spotify_songs (username, song_name, artist, rank) VALUES (?, ?, ?, ?)', (username, song_name, artist, rank))
    conn.commit()
    conn.close()

# Get songs from database
def get_songs(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM spotify_songs WHERE username = ?', (username,))
    songs = c.fetchall()
    conn.close()
    return songs

# Initialize database
init_db()

# Streamlit app
st.title('Xmas Quiz Registration')

# Register user
st.write('## Register')
username = st.text_input('Username')
email = st.text_input('Email')
dob = st.date_input('Date of birth')
birthplace = st.text_input('Place of birth')
if st.button('Register'):
    register_user(username, email, dob, birthplace)
    st.success('Registration successful! Check your email for verification.')

# Verify user
st.write('## Verify')
# Add song
st.write('## Add Song')
username = st.text_input('Username', key='add_song_username')
song_name = st.text_input('Song name')
artist = st.text_input('Artist')
rank = st.number_input('Rank')

if st.button('Add Song'):
    add_song(username, song_name, artist, rank)
    st.success('Song added to database!')

# Get songs
st.write('## Get Songs')
username = st.text_input('Username', key='get_songs_username')

if st.button('Get Songs'):
    songs = get_songs(username)
    if songs:
        for song in songs:
            st.write(song)
    else:
        st.write('No songs found for this user.')

# Display all songs
st.write('## All Songs')
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('SELECT * FROM spotify_songs')
all_songs = c.fetchall()
if all_songs:
    for song in all_songs:
        st.write(song)
else:
    st.write('No songs found in the database.')
conn.close()




