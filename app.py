from flask import Flask, render_template, request, jsonify
import requests
import yt_dlp
from bs4 import BeautifulSoup

app = Flask(__name__)

# Function to scrape search results from Spotify Web
def scrape_spotify_search(query):
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"https://open.spotify.com/search/{query.replace(' ', '%20')}"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    results = []
    for div in soup.find_all('div', {'class': 'Type__TypeElement'}):
        title = div.text
        if title:
            results.append({'title': title})
    return results[:10]

# Function to get YouTube playable link
def get_youtube_audio(query):
    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio/best',
        'default_search': 'ytsearch',
        'noplaylist': True,
        'forceurl': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        audio_url = info['url']
    return audio_url

@app.route('/')
def home():
    trending = scrape_spotify_search('Top 50')
    return render_template('home.html', trending=trending)

@app.route('/search')
def search():
    query = request.args.get('q')
    results = scrape_spotify_search(query)
    return render_template('search.html', results=results, query=query)

@app.route('/play', methods=['POST'])
def play_song():
    song = request.json.get('song')
    audio_url = get_youtube_audio(song)
    return jsonify({'audio_url': audio_url})

# Static artist and album pages for now
@app.route('/artist/<artist_name>')
def artist(artist_name):
    return render_template('artist.html', artist_name=artist_name)

@app.route('/album/<album_name>')
def album(album_name):
    return render_template('album.html', album_name=album_name)

if __name__ == "__main__":
    app.run(debug=True)
