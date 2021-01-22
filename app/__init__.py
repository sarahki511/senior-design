from flask import Flask
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '\xd8\xf1\xa5\xdd\x8eD\xf7\xdf]\xe7\x05\xf79\xa3\x0e\xd1'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'csv'}
app.config['EMAIL_ID'] = os.environ.get('EMAIL_ID')
app.config['EMAIL_PWD'] = os.environ.get('EMAIL_PWD')
app.config['IMAGE_UPLOADS'] = 'app/static/image'
app.config['IMAGE_DOWNLOADS'] = 'app/static/uploads'

from app import views