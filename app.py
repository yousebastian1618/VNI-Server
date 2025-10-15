from __future__ import annotations
from flask import Flask, jsonify, request, make_response
from dotenv import load_dotenv

from domains.maintenance.models import Maintenance

load_dotenv()
from strawberry.flask.views import GraphQLView
from config import Config
from schema import schema
from extensions import db, migrate, mail
from flask_cors import CORS
import sqlite3
from sqlalchemy import event
from sqlalchemy.engine import Engine
from domains.product.services import product_bp
from domains.blog.services import blog_bp


def create_app() -> Flask:
  app = Flask(__name__)

  app.config.from_object(Config)
  db.init_app(app)
  migrate.init_app(app, db)
  mail.init_app(app)

  CORS(
    app,
    resources={r"/*": {
      "origins": [Config.CLIENT, "https://*.pages.dev/"],
      "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
      "allow_headers": ["Content-Type", "Authorization"],
      "expose_headers": ["Content-Type"],
      "supports_credentials": True,
    }}
  )

  allowed_requests = ['Maintenance', 'Login', 'ToggleMaintenance', 'GetUserByToken']

  @app.before_request
  def maintenance_gate():
    if request.method == 'OPTIONS':
      return make_response("", 204)
    m = Maintenance.query.first()
    if m and m.maintenance:
      op = None
      if request.method == "POST":
        data = request.get_json(silent=True) or {}
        op = data.get("operationName")
      elif request.method == 'GET':
        op = request.args.get("operationName")
      if op in allowed_requests:
        return
      return jsonify({"status": "UNDER_MAINTENANCE"}), 503
    return
    # if Maintenance.query.first().maintenance:
    #   if request.method == "POST":
    #     payload = request.get_json(silent=True)
    #   else:
    #     q = request.args.get("query")
    #     payload = {"query": q} if q else None
    #   if 'operationName' in payload:
    #     if payload['operationName'] in allowed_requests:
    #       return
    #   return jsonify({"status": "UNDER_MAINTENANCE"}), 503
    # return

  @event.listens_for(Engine, "connect")
  def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
      cursor = dbapi_connection.cursor()
      cursor.execute("PRAGMA foreign_keys=ON")
      cursor.close()

  app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql_view", schema=schema, graphiql=Config.ENV == 'local'),
    methods=["GET", "POST", "OPTIONS"]
  )
  app.register_blueprint(product_bp)
  app.register_blueprint(blog_bp)

  @app.get("/")
  def health():
    current_env = Config.ENV
    if current_env == 'local':
      return {"status": "ok", "graphql": "/graphql"}
    return {"status": "ok", "e": Config.ENV}

  return app
