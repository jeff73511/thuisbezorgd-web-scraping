import pytest
from sqlalchemy import create_engine


@pytest.fixture()
def test_engine(tmpdir):
    """"""
    return create_engine(f"sqlite:///{tmpdir}/thuisbezorgd.db")


@pytest.fixture()
def address():
    """"""
    return "Plesmanlaan 121, 1066 CX Amsterdam"


@pytest.fixture()
def cuisines():
    """"""
    return ["Fries", "Snacks", "Wok"]
