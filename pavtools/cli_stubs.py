from typer import Typer

from pavtools.errors import try_import

app = Typer()


@app.command()
@try_import('pavaudio')
def extract_audio():
    """Extracts the audio from a video."""


@app.command()
@try_import('pavaudio')
def cut_silences():
    """Removes all silences from an audio file."""


@app.command()
@try_import('pavaudio')
def audio_processing():
    """Apply vst effects on audio."""
