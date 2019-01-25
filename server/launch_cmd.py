#!/usr/bin/env python

from server import create_app

from model import db, User, Tool


app = create_app()
app_context = app.app_context()
app_context.push()
app.client = app.test_client()
db.app = app
