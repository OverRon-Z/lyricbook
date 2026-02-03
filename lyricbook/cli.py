import typer
from pathlib import Path
import json

app = typer.Typer()

DATA_FILE = Path.home() / ".lyricbook.json"


def load_data():
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


@app.command()
def add(artist: str, song: str, lyrics: str):
    """Add a new song to your lyricbook."""
    data = load_data()
    data.append({
        "artist": artist,
        "song": song,
        "lyrics": lyrics
    })
    save_data(data)
    typer.echo(f"Added: {artist} - {song}")


@app.command()
def list():
    """List all saved songs."""
    data = load_data()
    if not data:
        typer.echo("No songs saved yet.")
        return

    for i, entry in enumerate(data, 1):
        typer.echo(f"{i}. {entry['artist']} - {entry['song']}")


@app.command()
def search(term: str):
    """Search lyrics for a word or phrase."""
    data = load_data()
    results = [
        entry for entry in data
        if term.lower() in entry["lyrics"].lower()
    ]

    if not results:
        typer.echo("No matches found.")
        return

    for entry in results:
        typer.echo(f"{entry['artist']} - {entry['song']}")


@app.command()
def view(artist: str, song: str):
    """View lyrics for a specific song."""
    data = load_data()
    for entry in data:
        if entry["artist"] == artist and entry["song"] == song:
            typer.echo(f"\n{artist} - {song}\n")
            typer.echo(entry["lyrics"])
            return

    typer.echo("Song not found.")

import lyricsgenius
import os

# Genius client
GENIUS_TOKEN = os.environ.get("GENIUS_TOKEN")
genius = lyricsgenius.Genius(GENIUS_TOKEN, skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"], remove_section_headers=True)

@app.command()
def fetch(artist: str, song: str):
    """Fetch lyrics from Genius and add to your lyricbook."""
    if not GENIUS_TOKEN:
        typer.echo("Error: GENIUS_TOKEN environment variable not set.")
        raise typer.Exit()

    try:
        song_obj = genius.search_song(song, artist)
        if not song_obj or not song_obj.lyrics:
            typer.echo("Lyrics not found.")
            return
        lyrics = song_obj.lyrics
        data = load_data()
        data.append({"artist": artist, "song": song, "lyrics": lyrics})
        save_data(data)
        typer.echo(f"Fetched and added: {artist} - {song}")
    except Exception as e:
        typer.echo(f"Error fetching lyrics: {e}")

if __name__ == "__main__":
    app()

