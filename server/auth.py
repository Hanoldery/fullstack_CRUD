import json

from functools import wraps
from flask import jsonify, request, Blueprint, current_app
# from flask_bcrypt import Bcrypt
auth = Blueprint('auth', __name__)

from model import db, User, datetime_handler
from mail import subscribe_mail, confirm_email


# TODO: Check this shit
def login_required(admin, api_restrict=False):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            return f(*args, **kwargs)
            data = request.get_json()
            if request.method == 'GET' and 'user' not in str(request):
                return f(*args, **kwargs)
            if data is None or data.get('email') is None or data.get('auth_token') is None:
                return 'Not authorized, invalid request.', 401
            user = User.query.filter_by(email=data.get('email')).first()
            print(user, data)
            if user is None:
                return 'Not authorized, no user.', 401
            if user.decode_auth_token(data.get('auth_token')) != user.id:
                return 'Invalid token. Please log again.', 401
            if admin is True and user.admin is False:
                return 'Not authorized', 401
            if api_restrict is True:
                if 'user' not in str(request) or user.admin is True:
                    return f(*args, **kwargs)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@auth.route("/api/confirm/<token>", methods=['POST'])
def confirm(token):
    form = request.get_json()
    print('CONFIRM')
    if confirm_email(token, form.get('password')) is False:
        return jsonify({'message': "Something went wrong, please retry."}), 400
    return jsonify({'message': "Everything is registered and confirmed."}), 200


@auth.route("/api/login", methods=['POST'])
def login():
    post_data = request.get_json()
    user = User.query.filter_by(email=post_data.get('email')).first()
    if user and user.confirmed:
        print(current_app.bcrypt.check_password_hash(user.password, post_data.get('password')))
        if current_app.bcrypt.check_password_hash(
            user.password, post_data.get('password')
        ):
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                response = {
                    'message': 'Successfully logged in.',
                    'auth_token': auth_token.decode(),
                    'email': user.email,
                    'title': user.title,
                    'admin': user.admin,
                    'id': user.id,
                }
                return jsonify(response), 200
        else:
            return jsonify({'message': 'Wrong credentials.'}), 400
    elif user and user.confirmed is False:
        subscribe_mail(user)
        return jsonify({'message': 'You have an account but didn\'t confirmed it.<br/> Please check you emails.'}), 400
    else:
        return jsonify({'message': 'User does not exist.'}), 404


@auth.route("/api/me", methods=['POST'])
def me():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''
    if auth_token:
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            user = User.query.filter_by(id=resp).first()
            responseObject = {
                'data': {
                    'user_id': user.id,
                    'email': user.email,
                    'admin': user.admin,
                    'registered_on': user.registered_on
                }
            }
            return jsonify(responseObject), 200
        responseObject = {
            'message': resp
        }
        return jsonify(responseObject), 401
    else:
        responseObject = {
            'message': 'Provide a valid auth token.'
        }
        return jsonify(responseObject), 401


@auth.route("/api/password_reset", methods=['POST'])
def password_reset():
    form = request.get_json()
    if form.get('email') is None:
        return jsonify({'message': 'The email field is empty or invalid.'}), 400
    user = User.query.filter_by(email=form.get('email')).first()
    if user:
        token = subscribe_mail(user)
        return jsonify({'message': 'We sent you an email to set your password.', 'token': token}), 200
    else:
        return jsonify({'message': 'There\'s no account with this email address.'}), 200


@auth.route("/api/register", methods=['POST'])
def register():
    form = request.get_json()
    if form.get('email') is None:
        return jsonify({'message': 'The email field is empty or invalid.'}), 400
    user = User.query.filter_by(email=form.get('email')).first()
    if user:
        if user.confirmed is False:
            token = subscribe_mail(user)
            return jsonify({'message': 'This account already exist <br/>We sent you another confirmation email. Check your inbox.', 'token': token}), 400
        else:
            return jsonify({'message': 'This account already exist <br/>You can connect with this email.'}), 400
    user = User(
        email=form.get('email'),
        title=form.get('title'),
        password='.',
        admin=False,
        confirmed=False
    )
    db.session.add(user)
    db.session.commit()
    token = subscribe_mail(user)
    return jsonify({'message': 'User registered.', 'token': token}), 200
