import sys
from functools import wraps
from importlib import import_module
from typing import Callable

from rich.console import Console

console = Console()


def try_import(module_name: str):
    def _inner(func: Callable):
        @wraps(func)
        def __inner(*args, **kwargs):
            try:
                kwargs['module'] = import_module(module_name)
            except ModuleNotFoundError:
                console.print(
                    f'[b]Please install {module_name}:[/]'
                    '\n\n'
                    f'[red]pipx install {module_name}[/]'
                    '\n\n'
                    'or [red]pipx install pavtools'
                    rf"\[{module_name.replace('pav', '')}][/]"
                )
                sys.exit()
            return func(*args, **kwargs)

        return __inner

    return _inner
