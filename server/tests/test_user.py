import json
import datetime
import re

from model import User


def test_user_exist(app):
    assert User.query.filter(User.password is not None).first() is not None


def test_encode_auth_token(app):
    user = User.query.filter(User.password is not None).first()
    auth_token = user.encode_auth_token(user.id)
    assert isinstance(auth_token, bytes)


def test_decode_auth_token(app):
    user = User.query.filter(User.password is not None).first()
    auth_token = user.encode_auth_token(user.id)
    assert isinstance(auth_token, bytes)
    assert user.decode_auth_token(auth_token) == user.id


def test_registered_user_register(app):
    response = app.client.post(
        '/api/register',
        data=json.dumps(dict(
            email='gerbaudp@gmail.com',
            name='pierre'
        )),
        content_type='application/json'
    )
    data = json.loads(response.data.decode())
    assert 'You can connect with this email.' in data['message']
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_unregistered_user_register(app):
    response = app.client.post(
        '/api/register',
        data=json.dumps(dict(
            email='test_' + re.sub(r"[\ |\-|\.|\:]", "", datetime.datetime.now().isoformat()) + '@gmail.com',
            name='pierre'
        )),
        content_type='application/json'
    )
    data = json.loads(response.data.decode())
    assert data['message'] == 'User registered.'
    assert response.content_type == 'application/json'
    assert data['token'] != ''
    assert response.status_code, 200

    # I do it twice for now, because of the other tests,
    # this could go in a fixture
    # TODO: Make this shit a fixture
    response = app.client.post(
        '/api/register',
        data=json.dumps(dict(
            email='test_' + re.sub(r"[\ |\-|\.|\:|1|2]", "", datetime.datetime.now().isoformat()) + '@gmail.com',
            name='pierre'
        )),
        content_type='application/json'
    )
    data = json.loads(response.data.decode())
    assert data['message'] == 'User registered.'
    assert response.content_type == 'application/json'
    assert data['token'] != ''
    assert response.status_code, 200


def test_unconfirmed_user_register(app):
    user = User.query.filter(User.email.contains('test'), User.confirmed == False).first()
    response = app.client.post(
        '/api/register',
        data=json.dumps(dict(
            email=user.email,
            name=user.email
        )),
        content_type='application/json'
    )
    data = json.loads(response.data.decode())
    'We sent you another confirmation email.' in data['message']
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_registered_user_login(app):
    user = User.query.filter_by(email="gerbaudp@gmail.com").first()
    assert user is not None

    response = app.client.post(
        '/api/login',
        data=json.dumps(dict(
            email='gerbaudp@gmail.com',
            password='lolilol'
        )),
        content_type='application/json'
    )
    data = json.loads(response.data.decode())
    assert data['message'] == 'Successfully logged in.'
    assert data['email'] == user.email
    assert data['admin'] == user.admin
    assert data['name'] == user.name
    assert user.decode_auth_token(data['auth_token']) == user.id
    assert response.content_type == 'application/json'
    assert response.status_code, 200


def test_unregistered_user_login(app):
    response = app.client.post(
        '/api/login',
        data=json.dumps(dict(
            email='neverexist@neverexist.neverexist',
            password='lolilol'
        )),
        content_type='application/json'
    )
    data = json.loads(response.data.decode())
    assert data['message'] == 'User does not exist.'
    assert response.content_type == 'application/json'
    assert response.status_code, 404


def test_unconfirmed_user_login(app):
    user = User.query.filter(User.email.contains('test'), User.confirmed == False).first()
    assert user is not None

    response = app.client.post(
        '/api/login',
        data=json.dumps(dict(
            email=user.email,
            password='lolilol'
        )),
        content_type='application/json'
    )
    data = json.loads(response.data.decode())
    assert 'You have an account but didn\'t confirmed it.' in data['message']
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_registered_user_login_wrong_credentials(app):
    user = User.query.filter_by(email="gerbaudp@gmail.com").first()
    assert user is not None

    response = app.client.post(
        '/api/login',
        data=json.dumps(dict(
            email='gerbaudp@gmail.com',
            password='wronganyway'
        )),
        content_type='application/json'
    )
    data = json.loads(response.data.decode())
    assert data['message'] == 'Wrong credentials.'
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_registered_user_password_reset(app):
    user = User.query.filter(User.email.contains('test'), User.confirmed == True).first()
    assert user is not None
    response = app.client.post(
        '/api/password_reset',
        data=json.dumps(dict(
            email=user.email
        )),
        content_type='application/json'
    )
    data = json.loads(response.data.decode())
    token = data['token']
    assert token != ''
    assert data['message'] == 'We sent you an email to set your password.'
    assert response.content_type == 'application/json'
    assert response.status_code, 200

    response = app.client.post(
        '/api/confirm/' + token,
        data=json.dumps(dict(
            password='test'
        )),
        content_type='application/json'
    )
    data = json.loads(response.data.decode())
    assert data['message'] == 'Everything is registered and confirmed.'
    assert response.content_type == 'application/json'
    assert response.status_code, 200


def test_unconfirmed_user_password_reset(app):
    user = User.query.filter(User.email.contains('test'), User.confirmed == False).first()
    assert user is not None
    response = app.client.post(
        '/api/password_reset',
        data=json.dumps(dict(
            email=user.email
        )),
        content_type='application/json'
    )
    data = json.loads(response.data.decode())
    token = data['token']
    assert token != ''
    assert data['message'] == 'We sent you an email to set your password.'
    assert response.content_type == 'application/json'
    assert response.status_code, 200

    response = app.client.post(
        '/api/confirm/' + token,
        data=json.dumps(dict(
            password='test'
        )),
        content_type='application/json'
    )
    data = json.loads(response.data.decode())
    assert data['message'] == 'Everything is registered and confirmed.'
    assert response.content_type == 'application/json'
    assert response.status_code, 200


def test_unregistered_user_password_reset(app):
    response = app.client.post(
        '/api/password_reset',
        data=json.dumps(dict(
            email='neverexist@neverexist.neverexist'
        )),
        content_type='application/json'
    )
    data = json.loads(response.data.decode())
    assert data['message'] == 'There\'s no account with this email address.'
    assert response.content_type == 'application/json'
    assert response.status_code, 400
