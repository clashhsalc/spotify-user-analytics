import streamlit as st
import pandas as pd
import json
import plotly.express as px

def load_data(file):
    data = json.load(file)
    df = pd.DataFrame(data)
    df['minutes_played'] = df['ms_played'] / 60000  
    df['device'] = df['platform'].apply(lambda x: x.split('(')[-1].split(',')[0].strip())
    return df

def display_top_songs(df):
    st.write("### Top Songs")
    top_songs = df.groupby('master_metadata_track_name')['minutes_played'].sum().sort_values(ascending=False).head(6).reset_index()
    for idx, row in top_songs.iterrows():
        st.write(f"{idx+1}. {row['master_metadata_track_name']} by {row['master_metadata_album_artist_name']} ({row['minutes_played']:.2f} minutes)")

def display_top_artists(df):
    st.write("### Top Artists")
    top_artists = df.groupby('master_metadata_album_artist_name')['minutes_played'].sum().sort_values(ascending=False).head(6).reset_index()
    for idx, row in top_artists.iterrows():
        st.write(f"{idx+1}. {row['master_metadata_album_artist_name']} ({row['minutes_played']:.2f} minutes)")

st.title("spotify nalytics ")
st.write("drag and drop your spotify data JSON file below:")

uploaded_file = st.file_uploader("choose a JSON file", type="json")
if uploaded_file is not None:
    df = load_data(uploaded_file)
    display_top_songs(df)
    display_top_artists(df)
