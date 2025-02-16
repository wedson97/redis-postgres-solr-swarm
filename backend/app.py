from flask import Flask
from flask_redis import FlaskRedis
from dotenv import load_dotenv
import os

from helpers.api import api, blueprint
from helpers.cors import cors
from helpers.database import db
import models

## Identificar 
if(os.environ.get("DATABASE_URL")==None):
    load_dotenv(".env.development")
    
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:123456@postgres:5432/cbo_ocupacao"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app=app)
cors.init_app(app=app)
api.init_app(app=app)

if __name__ == "__main__":
    app.run()