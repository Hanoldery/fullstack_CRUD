import os

# from flask import current_app
import sendgrid
from sendgrid.helpers.mail import *
from itsdangerous import URLSafeTimedSerializer
from python_http_client import exceptions
from flask import current_app, Blueprint

from model import User, db

sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))

mail = Blueprint('mail', __name__)


def print_response(response):
    print('RESPONSE')
    print(response.status_code)
    print(response.body)
    print(response.headers)


def subscribe_mail(user):
    mail = Mail()
    mail.from_email = Email("gerbaudp@gmail.com", "Myself")
    if (user.confirmed):
        mail.subject = "Welcome to Hans Zimmer's worlds !"
        mail.template_id = "ADD_TEMPLATE_ID"
    else:
        mail.subject = "Reset your password"
        mail.template_id = "ADD_TEMPLATE_ID"

    # We first create the personalization object
    # along with the receiver of the email
    perso = Personalization()
    perso.add_to(Email(user.email, user.title))
    mail.add_personalization(perso)
    data = mail.get()
    token = generate_confirmation_token(user.email)
    activate_link = os.environ['FRONT_URL'] + '/confirm/' + token
    print(activate_link)

    # We have to customize the JSON sent ourself as sendgrid
    # python API isn't good enough to send data through a tempalte
    data['personalizations'][0]['dynamic_template_data'] = {}
    data['personalizations'][0]['dynamic_template_data']['user_mail'] = user.email
    data['personalizations'][0]['dynamic_template_data']['user_name'] = user.title
    data['personalizations'][0]['dynamic_template_data']['user_token'] = activate_link

    print("DATA")
    print(data)

    try:
        response = sg.client.mail.send.post(request_body=data)
    except exceptions.BadRequestsError as e:
        print(e)
        return ''
    print_response(response)
    return token


def confirm_email(token, password):
    email = confirm_token(token)
    user = User.query.filter_by(email=email).first_or_404()
    user.confirmed = True
    user.password = current_app.bcrypt.generate_password_hash(password).decode('utf-8')
    db.session.add(user)
    db.session.commit()
    return True


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(os.environ['SECRET_KEY'])
    return serializer.dumps(email, salt=os.environ['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=36000):
    serializer = URLSafeTimedSerializer(os.environ['SECRET_KEY'])
    # try:
    email = serializer.loads(
        token,
        salt=os.environ['SECURITY_PASSWORD_SALT'],
        max_age=expiration
    )
    # except(exception) as e:
    #     print(e)
    return email
