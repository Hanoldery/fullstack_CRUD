from flask import current_app, jsonify


class InvalidTokenError(Exception):
    def __init__(self):
        self.msg = 'Invalid token'

    def __str__(self):
        return repr(self.msg)


class AlreadyExistError(Exception):
    def __init__(self, obj, msg):
        self.obj = obj
        self.msg = msg

    def __str__(self):
        return repr(self.obj, self.msg)


class EmptyError(Exception):
    def __init__(self, obj):
        self.obj = obj

    def __str__(self):
        return repr(self.obj)


@current_app.errorhandler(EmptyError)
def handle_empty(error):
    return jsonify({'message': 'The field ' + error.obj + ' is empty or invalid.'}), 400


@current_app.errorhandler(InvalidTokenError)
def handle_invalid_token(error):
    return jsonify({'message': 'The token is invalid or expired.'}), 400


@current_app.errorhandler(AlreadyExistError)
def handle_already_exist(error):
    return jsonify({'message': 'This ' + error.obj + ' already exist.' + error.msg}), 400
