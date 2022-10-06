from flask import Flask
from models import db
from flask_migrate import Migrate
from routes.routes import api,socketio
from schemas import ma


SECRET_KEY = 'eb38195ecc20b6675a4868e8f79c0d0b'

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"]='mysql+pymysql://root:root@localhost/chat_db'

app.config['SECRET_KEY']=SECRET_KEY


app.register_blueprint(api)


db.init_app(app)


ma.init_app(app)

socketio.init_app(app)


migrate = Migrate(app,db)




