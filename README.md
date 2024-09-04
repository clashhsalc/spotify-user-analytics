# Spotify Data Analytics Dashboard

A web app that analyzes and visualizes your spotify listening data.

## Features

- Basic analytics (total tracks, total time played etc.)
- View your latform and device usage history
- View your most played tracks and artists
- Analyze genre distribution
- View listening patterns by time of day
- View listening location history

## Getting Your Spotify Data

Before using this dashboard, you need to request your data from Spotify:

1. Go to your Spotify account page (https://www.spotify.com/account)
2. Navigate to Privacy Settings
3. Scroll down to "Download your data" and click "Request"
4. Wait for Spotify to process your request (this can take up to 4 weeks)
5. Once ready, download your data and extract the JSON file

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
#### Dependencies
- Python 3.x
- pandas==2.2.2
- plotly==5.22.0
- streamlit==1.36.0


## Usage

1. Run the app:
   ```
   streamlit run main.py
   ```
2. Open the localhost link on your browser or wait for it to redirect automatically.
3. Upload your Spotify data JSON file







