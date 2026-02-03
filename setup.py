from setuptools import setup, find_packages

setup(
    name="lyricbook",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "typer>=0.21.1",
        "lyricsgenius>=3.0.1",
        "rich>=14.3.2"
    ],
    entry_points={
        "console_scripts": [
            "lyricbook=lyricbook.cli:app",
        ],
    },
    python_requires=">=3.10",
)

