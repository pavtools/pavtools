import pytest
from pavtools.errors import try_import


def test_try_import(capsys):
    captured = capsys.readouterr()

    @try_import('batata')
    def func():
        ...

    with pytest.raises(SystemExit):
        func()

        assert (
            captured.out
            == """Please install batata:

pipx install batata

or pipx install pavtools[batata]"""
        )
