import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_uploads import UploadSet, IMAGES, configure_uploads
from algoliasearch import algoliasearch



def create_app():
    app = Flask(__name__)
    DATABASE_URI = 'postgresql://' + os.environ['DATABASE_LOGIN'] + ':'\
        + os.environ['DATABASE_PASSWORD'] + '@'\
        + os.environ['DATABASE_HOST'] + '/'\
        + os.environ['DATABASE_NAME']
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    print(DATABASE_URI)
    # Avoid SQLAlchemy to track when objects changes.
    # Will be disabled by default in the future
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['UPLOADED_PHOTOS_DEST'] = os.environ['APP_DIRECTORY'] + 'static/img/'
    photos = UploadSet('photos', IMAGES)
    configure_uploads(app, (photos,))

    from model import db
    db.init_app(app)
    app.db = db
    app.photos = photos

    app.algoClient = algoliasearch.Client("ADD_CLIENT_ID", 'ADD_KEY_ID')
    app.indexMedia = app.algoClient.init_index('media')
    app.indexNews = app.algoClient.init_index('news')
    app.indexArtist = app.algoClient.init_index('artist')

    with app.app_context():
        from auth import auth
        from crud import crud
    app.register_blueprint(auth)
    app.register_blueprint(crud)

    app.bcrypt = Bcrypt(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=4000, debug=True)
