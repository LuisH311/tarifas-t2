import pytest

from app.historial import _historiales


@pytest.fixture(autouse=True)
def limpiar_historiales():
    _historiales.clear()
    yield
    _historiales.clear()
