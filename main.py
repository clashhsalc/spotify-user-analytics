import streamlit as st
import pandas as pd
import json

def load_data(file):
    data = json.load(file)
    df = pd.DataFrame(data)
    df['minutes_played'] = df['ms_played'] / 60000  
    df['device'] = df['platform'].apply(lambda x: x.split('(')[-1].split(',')[0].strip())
    return df

def display_analytics(df):
    st.write("## Basic Analytics")
    st.write(f"Total Tracks Played: {len(df)}")
    st.write(f"Total Time Played (minutes): {df['minutes_played'].sum():.2f}")
    st.write(f"Unique Tracks Played: {df['spotify_track_uri'].nunique()}")
    st.write(f"Unique Artists: {df['master_metadata_album_artist_name'].nunique()}")
    st.write("### Unique Platforms")
    unique_platforms = df['platform'].value_counts()
    st.bar_chart(unique_platforms)
    st.write(unique_platforms.to_frame().reset_index().rename(columns={'index': 'Platform', 'platform': 'Count'}))
    st.write("### Unique Devices")
    unique_devices = df['device'].value_counts()
    st.bar_chart(unique_devices)
    st.write(unique_devices.to_frame().reset_index().rename(columns={'index': 'Device', 'device': 'Count'}))
    st.write("### Most Played Tracks")
    most_played_tracks = df.groupby('master_metadata_track_name')['minutes_played'].sum().sort_values(ascending=False).head(10)
    st.bar_chart(most_played_tracks)
    st.write(most_played_tracks.to_frame().reset_index().rename(columns={'master_metadata_track_name': 'Track Name', 'minutes_played': 'Minutes Played'}))
    st.write("### Most Played Artists")
    most_played_artists = df.groupby('master_metadata_album_artist_name')['minutes_played'].sum().sort_values(ascending=False).head(10)
    st.bar_chart(most_played_artists)
    st.write(most_played_artists.to_frame().reset_index().rename(columns={'master_metadata_album_artist_name': 'Artist Name', 'minutes_played': 'Minutes Played'}))

st.title("spotify analytics")
st.write("drag and drop your spotify data JSON file below:")
uploaded_file = st.file_uploader("Choose a JSON file", type="json")
if uploaded_file is not None:
    df = load_data(uploaded_file)
    display_analytics(df)
