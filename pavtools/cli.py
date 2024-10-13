from ast import literal_eval
from json import dump
from itertools import chain
from pathlib import Path
from os import sep

from appdirs import AppDirs
from typer import Exit, Typer
from InquirerPy import inquirer
from InquirerPy.validator import PathValidator
from pedalboard import load_plugin

from pavtools.cli_stubs import app as stub_app

app = Typer(help='PAVtools!', no_args_is_help=True)
dirs = AppDirs('sigchain', 'pavtools')
config_path = Path(dirs.user_config_dir)

app.registered_commands += stub_app.registered_commands


def safe_eval_plugin(plugin, param) -> float | bool | str:
    try:
        return literal_eval(str(getattr(plugin, param)))
    except:
        return str(getattr(plugin, param))


def home_user() -> str:
    home = Path().home()
    return str(home) + sep


@app.command()
def config():
    config_data = {'plugins': {}}

    # select vst path
    vst_dir = inquirer.filepath(
        message='select vst path (press tab): ',
        only_directories=True,
        validate=PathValidator(
            is_dir=True, message='Input is not a directory'
        ),
        default=home_user(),
    ).execute()

    # select function
    vst_path = Path(vst_dir)
    plugins_path = list(chain(vst_path.glob('*.vst3'), vst_path.glob('*.au')))
    if plugins_path:
        selected_plugins = inquirer.rawlist(
            message='Pick your favourites:',
            choices=plugins_path,
            multiselect=True,
        ).execute()
    else:
        raise Exit(1)

    # Configure plugins
    for plugin in selected_plugins:
        plugin = str(plugin)
        loaded_plugin = load_plugin(plugin)
        loaded_plugin.show_editor()
        # BUG: https://github.com/spotify/pedalboard/issues/243
        config_data['plugins'][plugin] = {
            key: safe_eval_plugin(loaded_plugin, key)
            for key in loaded_plugin.parameters.keys()
        }

    # plugin chain
    selected_plugins = list(config_data['plugins'].keys())
    plugin_chain = []

    for plugin in config_data['plugins']:
        action = inquirer.fuzzy(
            message='Select order',
            choices=selected_plugins,
        ).execute()
        selected_plugins.remove(action)
        plugin_chain.append(action)

    # Save config
    config_path.mkdir(exist_ok=True, parents=True)
    config_data['vst_dir'] = vst_dir
    config_data['plugin_chain'] = plugin_chain
    with open(config_path / 'config.json', 'w') as config_file:
        dump(config_data, config_file)


try:
    from pavaudio.cli import app as audio_cli

    app.registered_commands += audio_cli.registered_commands
except:
    ...
