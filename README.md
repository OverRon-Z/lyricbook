# LyricBook

LyricBook is a terminal-based personal lyrics library built in Python.  
It allows you to **add, fetch, list, search, and view lyrics** directly from your terminal.

This project demonstrates building a **fully functional CLI tool** with persistence and API integration.

---

## Features

- **Add** lyrics manually  
- **Fetch** lyrics automatically from [Genius](https://genius.com)  
- **List** all saved songs  
- **Search** lyrics for a word or phrase  
- **View** full lyrics of a song  

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/OverRon-Z/lyricbook.git
cd lyricbook
Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate
Install dependencies:

pip install -r requirements.txt
Set your Genius API token (required for fetch):

export GENIUS_TOKEN="YOUR_GENIUS_API_TOKEN"

Usage
Add a song manually:
python -m lyricbook.cli add "Artist Name" "Song Title" "Lyrics..."

Example:
python -m lyricbook.cli add "Radiohead" "Creep" "I'm a creep, I'm a weirdo..."

Fetch lyrics automatically from Genius:
python -m lyricbook.cli fetch "Artist Name" "Song Title"

Example:
python -m lyricbook.cli fetch "Radiohead" "Creep"

List all saved songs:
python -m lyricbook.cli list

View lyrics of a specific song:
python -m lyricbook.cli view "Artist Name" "Song Title"

Search lyrics for a word or phrase:
python -m lyricbook.cli search "word"

Project Structure
lyricbook/
├── README.md
├── requirements.txt
├── venv/
└── lyricbook/
    ├── __init__.py
    └── cli.py
Notes:

All lyrics are stored locally in ~/.lyricbook.json

Make sure your virtual environment is active when running commands

Genius API token is required only for the fetch command
