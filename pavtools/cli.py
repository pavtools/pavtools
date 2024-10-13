from typer import Typer

from pavtools.cli_stubs import app as stub_app

app = Typer(help='PAVtools!', no_args_is_help=True)

app.registered_commands += stub_app.registered_commands


try:
    from pavaudio.cli import app as audio_cli

    app.registered_commands += audio_cli.registered_commands
except:
    ...
