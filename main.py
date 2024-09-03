import streamlit as st
import pandas as pd
import json
import plotly.express as px

def load_data(file):
    data = json.load(file)
    df = pd.DataFrame(data)
    df['minutes_played'] = df['ms_played'] / 60000 
    df['device'] = df['platform'].apply(lambda x: x.split('(')[-1].split(',')[0].strip())
    df['genre'] = df['master_metadata_album_album_name'].apply(lambda x: detect_genre(x))
    df['time_of_day'] = pd.to_datetime(df['ts']).dt.hour
    df['location'] = df['conn_country']
    
    return df

def detect_genre(album_name):
    if pd.isna(album_name):
        return 'Unknown'
    elif "Heartbreak" in album_name:
        return "Pop"
    elif "Revival" in album_name:
        return "Hip-hop"
    else:
        return "Other"

def display_analytics(df):
    st.write("## basic analytics")
    st.write(f"total tracks played: {len(df)}")
    st.write(f"total time played (minutes): {df['minutes_played'].sum():.2f}")
    st.write(f"unique tracks played: {df['spotify_track_uri'].nunique()}")
    st.write(f"unique artists: {df['master_metadata_album_artist_name'].nunique()}")
    st.write("### unique platforms")
    unique_platforms = df['platform'].value_counts().reset_index()
    unique_platforms.columns = ['platform', 'count']
    fig_platforms = px.bar(unique_platforms, x='platform', y='count', text='count', title='unique platforms', labels={'platform': 'platform', 'count': 'count'})
    fig_platforms.update_layout(title_text='unique platforms', title_x=0.5)
    st.plotly_chart(fig_platforms)
    st.write(unique_platforms)
    st.write("### unique devices")
    unique_devices = df['device'].value_counts().reset_index()
    unique_devices.columns = ['device', 'count']
    fig_devices = px.bar(unique_devices, x='device', y='count', text='count', title='unique devices', labels={'device': 'device', 'count': 'count'})
    fig_devices.update_layout(title_text='unique devices', title_x=0.5)
    st.plotly_chart(fig_devices)
    st.write(unique_devices)
    st.write("### most played tracks")
    most_played_tracks = df.groupby('master_metadata_track_name')['minutes_played'].sum().sort_values(ascending=False).head(10).reset_index()
    fig_tracks = px.bar(most_played_tracks, x='master_metadata_track_name', y='minutes_played', text='minutes_played', labels={'master_metadata_track_name': 'track name', 'minutes_played': 'minutes played'})
    fig_tracks.update_layout(title_text='most played tracks', title_x=0.5)
    st.plotly_chart(fig_tracks)
    st.write(most_played_tracks.rename(columns={'master_metadata_track_name': 'track name', 'minutes_played': 'minutes played'}))
    st.write("### most played artists")
    most_played_artists = df.groupby('master_metadata_album_artist_name')['minutes_played'].sum().sort_values(ascending=False).head(10).reset_index()
    fig_artists = px.bar(most_played_artists, x='master_metadata_album_artist_name', y='minutes_played', text='minutes_played', labels={'master_metadata_album_artist_name': 'artist name', 'minutes_played': 'minutes played'})
    fig_artists.update_layout(title_text='most played artists', title_x=0.5)
    st.plotly_chart(fig_artists)
    st.write(most_played_artists.rename(columns={'master_metadata_album_artist_name': 'artist name', 'minutes_played': 'minutes played'}))
    st.write("### genre analysis")
    genre_counts = df['genre'].value_counts().reset_index()
    genre_counts.columns = ['genre', 'count']
    fig_genre = px.bar(genre_counts, x='genre', y='count', text='count', title='genre distribution', labels={'genre': 'genre', 'count': 'count'})
    fig_genre.update_layout(title_text='genre distribution', title_x=0.5)
    st.plotly_chart(fig_genre)
    st.write(genre_counts)
    st.write("### time of day analysis")
    time_counts = df['time_of_day'].value_counts().sort_index().reset_index()
    time_counts.columns = ['hour', 'count']
    fig_time = px.line(time_counts, x='hour', y='count', title='listening time distribution', labels={'hour': 'hour of day', 'count': 'count'})
    fig_time.update_layout(title_text='listening time distribution', title_x=0.5)
    st.plotly_chart(fig_time)
    st.write(time_counts)
    st.write("### location analysis")
    location_counts = df['location'].value_counts().reset_index()
    location_counts.columns = ['country', 'count']
    fig_location = px.choropleth(location_counts, locations='country', locationmode='country names', color='count', hover_name='country', title='listening locations')
    fig_location.update_layout(title_text='listening locations')
    st.write(location_counts)


st.title("spotify data analytics dashboard")
st.write("drag and drop your spotify data json file below:")

uploaded_file = st.file_uploader("choose a json file", type="json")
if uploaded_file is not None:
    df = load_data(uploaded_file)
    display_analytics(df)
