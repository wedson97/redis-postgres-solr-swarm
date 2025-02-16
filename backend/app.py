from flask import Flask
from flask_redis import FlaskRedis
from dotenv import load_dotenv
import os

from helpers.api import api, blueprint
from helpers.cors import cors
from helpers.database import db
import models

# Carregar variáveis de ambiente para o desenvolvimento, se necessário
if os.environ.get("DATABASE_URL") is None:
    load_dotenv(".env.development")

# Inicializar o app Flask
app = Flask(__name__)

# Usar DATABASE_URL se estiver definido nas variáveis de ambiente, ou configurar diretamente a URI
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "postgresql://postgres:123456@postgres:5432/cbo_ocupacao")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização dos componentes
db.init_app(app=app)
cors.init_app(app=app)
api.init_app(app=app)

# Inicializar Redis se for necessário
if os.environ.get("REDIS_URL"):
    app.config['REDIS_URL'] = os.getenv("REDIS_URL", "redis://redis:6379/0")
    redis = FlaskRedis(app)

if __name__ == "__main__":
    # Rodar o app Flask
    app.run(host="0.0.0.0", port=5000, debug=True)
