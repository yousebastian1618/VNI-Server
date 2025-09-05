from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from botocore.context import get_context
from flask import Flask
from strawberry.flask.views import GraphQLView
from config import Config
from schema import schema
from extensions import db, migrate
from dotenv import load_dotenv
from flask_cors import CORS
import sqlite3
from sqlalchemy import event
from sqlalchemy.engine import Engine
from domains.product.services import product_bp


load_dotenv()

def create_app() -> Flask:
  app = Flask(__name__)
  CORS(
    app,
    resources={r"/*": {
      "origins": ["http://localhost:4202", "http://127.0.0.1:4202"],
      "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
      "allow_headers": ["Content-Type", "Authorization"],
      "expose_headers": ["Content-Type"],
    }}
  )

  app.config.from_object(Config)
  db.init_app(app)
  migrate.init_app(app, db)

  @event.listens_for(Engine, "connect")
  def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
      cursor = dbapi_connection.cursor()
      cursor.execute("PRAGMA foreign_keys=ON")
      cursor.close()

  app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql_view", schema=schema, graphiql=True)
  )
  app.register_blueprint(product_bp)

  @app.get("/")
  def health():
    return {"status": "ok", "graphql": "/graphql"}

  return app
