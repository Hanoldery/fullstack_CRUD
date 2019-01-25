import pytest

from server import create_app


@pytest.fixture
def app():
    app = create_app()
    app_context = app.app_context()
    app_context.push()
    app.db.create_all()
    app.client = app.test_client()
    return app


def test_conf(app):
    assert app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] is False
