import typer
from pathlib import Path
import json
import lyricsgenius
import os
import re

app = typer.Typer()

# Local storage
DATA_FILE = Path.home() / ".lyricbook.json"

# Genius API setup
GENIUS_TOKEN = os.environ.get("GENIUS_ACCESS_TOKEN")
genius = lyricsgenius.Genius(
    GENIUS_TOKEN,
    skip_non_songs=True,
    excluded_terms=["(Remix)", "(Live)"],
    remove_section_headers=True
)

# Helpers
def load_data():
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def song_exists(data, artist, song):
    return any(e["artist"].lower() == artist.lower() and e["song"].lower() == song.lower() for e in data)

def is_english(text):
    """Simple check if the text is mostly English letters"""
    letters = re.findall(r"[a-zA-Z]", text)
    return len(letters) / max(len(text), 1) > 0.5

# CLI commands
@app.command()
def add(artist: str, song: str, lyrics: str):
    """Add a new song manually to your lyricbook."""
    data = load_data()
    if song_exists(data, artist, song):
        typer.echo(f"Song '{artist} - {song}' already exists.")
        return
    data.append({"artist": artist, "song": song, "lyrics": lyrics})
    save_data(data)
    typer.echo(f"Added: {artist} - {song}")

@app.command()
def fetch(artist: str, song: str):
    """Fetch lyrics from Genius and add to your lyricbook (English only)."""
    if not GENIUS_TOKEN:
        typer.echo("Error: GENIUS_ACCESS_TOKEN environment variable not set.")
        raise typer.Exit()

    data = load_data()
    if song_exists(data, artist, song):
        typer.echo(f"Song '{artist} - {song}' already exists.")
        return

    try:
        song_obj = genius.search_song(song, artist)
        if not song_obj or not song_obj.lyrics:
            typer.echo("Lyrics not found.")
            return

        if not is_english(song_obj.lyrics):
            typer.echo(f"Skipping '{artist} - {song}' (non-English lyrics).")
            return

        data.append({"artist": artist, "song": song, "lyrics": song_obj.lyrics})
        save_data(data)
        typer.echo(f"Fetched and added: {artist} - {song}")
    except Exception as e:
        typer.echo(f"Error fetching lyrics: {e}")

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
def view(artist: str, song: str):
    """View lyrics for a specific song."""
    data = load_data()
    for entry in data:
        if entry["artist"].lower() == artist.lower() and entry["song"].lower() == song.lower():
            typer.echo(f"\n{artist} - {song}\n")
            typer.echo(entry["lyrics"])
            return
    typer.echo("Song not found.")

@app.command()
def search(term: str):
    """Search lyrics for a word or phrase."""
    data = load_data()
    results = [e for e in data if term.lower() in e["lyrics"].lower()]
    if not results:
        typer.echo("No matches found.")
        return
    for entry in results:
        typer.echo(f"{entry['artist']} - {entry['song']}")

@app.command()
def remove(artist: str, song: str):
    """Remove a song from your lyricbook."""
    data = load_data()
    new_data = [e for e in data if not (e["artist"].lower() == artist.lower() and e["song"].lower() == song.lower())]

    if len(new_data) == len(data):
        typer.echo(f"Song '{artist} - {song}' not found.")
        return

    save_data(new_data)
    typer.echo(f"Removed: {artist} - {song}")

if __name__ == "__main__":
    app()

