import os
from flask import Flask, redirect, render_template, request
from controllers.auth_controller import auth
from controllers.errors_controller import err_handler
from controllers.account_controller import account
from controllers.transaction_controller import transactions

from controllers.middlewares.auth_middlewares import token_required
from services.mail_service import MailService

app = Flask(__name__)

app.register_blueprint(auth)
app.register_blueprint(err_handler)
app.register_blueprint(account)
app.register_blueprint(transactions)

app.config['DNS_NAME'] = os.environ.get('DNS_NAME') or 'localhost:3000' #TODO define DNS_NAME

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'ufh4197y2f35y8h234f80uv13h8015jv34' 
app.config['AES_SECRET_KEY'] = os.environ.get('AES_SECRET_KEY') or 'nv12534n502482048y5b0iu2485n0bv82'
app.config['DATABASE'] = os.environ.get('DATABASE') or './db/sqlite.db'
app.config['CLEAR_DB'] = True

app.config['MAIL_SERVER']= os.environ.get('MAIL_SERVER') or 'smtp.office365.com'
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT') or 587
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME') or '-'
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD') or '-'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

@app.route("/", methods=["GET"])
def index():
    if "Authorization" in request.cookies:
        return redirect("/main")
    return render_template("index.html")


@app.route("/main", methods=["GET"])
@token_required
def main(current_user):
    return render_template("main.html", user=current_user)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=3000)
