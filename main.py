from flask import Flask, _app_ctx_stack, jsonify, make_response, json
from flask_cors import CORS
from sqlalchemy.orm import scoped_session
from werkzeug.exceptions import HTTPException

from app import models
from app.controllers.PostalCodeController import PostalCodeController
from app.controllers.UptimeController import UptimeController
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = Flask(__name__)
CORS(app)
app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)


@app.cli.command("deploy-script")
def deploy_script():
    UptimeController.run_sql_script()


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    data = dict(
        message=e.description,
    )
    return jsonify(data), e.code


@app.route('/status')
def status_application():
    return jsonify(UptimeController.get())


@app.route('/postal-codes')
def get_postal_codes():
    result = PostalCodeController.get_all()
    response = make_response(json.dumps(result['data']))
    response.headers['Content-Type'] = 'application/json'
    response.headers['x-total-count'] = result['total']
    return response


@app.route('/postal-codes/<code>')
def get_postal_code(code):
    return jsonify(PostalCodeController.get(code))


if __name__ == "__main__":
    from os import environ

    debug = (environ.get("DEBUG") == 'true')
    port = int(environ.get("PORT", 5000))
    host = environ.get("HOST", '127.0.0.1')

    app.run(debug=debug, port=port, host=host)
