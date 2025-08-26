from flask import Flask
from strawberry.flask.views import GraphQLView
from config import Config
from schema import schema
from extensions import db, migrate
from dotenv import load_dotenv

load_dotenv()

def create_app() -> Flask:
  app = Flask(__name__)
  app.config.from_object(Config)
  db.init_app(app)
  migrate.init_app(app, db)

  with app.app_context():
    from domains.blog import models

  app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql_view", schema=schema, graphiql=True)
  )

  @app.get("/")
  def health():
    return {"status": "ok", "graphql": "/graphql"}

  return app
