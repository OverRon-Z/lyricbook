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


if __name__ == "__main__":
    app()

