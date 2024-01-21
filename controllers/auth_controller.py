import random
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    make_response,
    current_app,
)
from app_settings import AppSettings

from controllers.forms.password_restore_request_form import PasswordRestoreRequestForm
from controllers.forms.registration_form import RegistrationForm
from controllers.forms.login_form import LoginForm
from controllers.errors_controller import internal_server_error, page_not_found, unauthorized
from services.hash_service import HashService

from services.jwt_service import JWTService
from services.mail_service import MailService
from services.password_restore_service import PasswordRestoreService
from services.tries_service import TriesService
from services.user_service import UserService

auth = Blueprint("auth", __name__, template_folder="templates")


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    requested_numbers = random.sample(range(8), AppSettings().get("auth_mask_len"))
    fill = [(x in requested_numbers) for x in range(8)]

    if request.method == "GET":
        return render_template("auth/login.html", form=form, fill=fill)

    if request.method == "POST":
        ip_addr = request.remote_addr
        username = form.username.data
        password = form.password.data
        user_id, logged = UserService().login(username=username, password=password)

        digits = [
            form.digit_0.data,
            form.digit_1.data,
            form.digit_2.data,
            form.digit_3.data,
            form.digit_4.data,
            form.digit_5.data,
            form.digit_6.data,
            form.digit_7.data,
        ]
        if logged:
            document_number = UserService().get_user_document(user_id)
            if not all([digits[i] == None or digits[i] == document_number[i] for i in range(8)]):
                logged = False
                user_id = None
                return render_template(
                    "auth/login.html",
                    form=form,
                    fill=fill,
                    msg="Invalid username or password",
                    msg_type="error",
                )
        last_try_id = TriesService().add(user_id, ip_addr)
        failed_tries = TriesService().get_failed_tries_count(user_id)

        if failed_tries >= AppSettings().get("auth_tries"):
            return render_template(
                "auth/login.html",
                form=form,
                fill=fill,
                msg="Too many failed logins, try again in 1 hour",
                msg_type="error",
            )
        if logged:
            try:
                token = JWTService().encode(user_id, username, ip_addr)
                resp = redirect("/main")
                resp.set_cookie("Authorization", token)
                TriesService().make_sucess(last_try_id)
                return resp
            except Exception as e:
                return internal_server_error(e)
        elif user_id is None:
            return render_template(
                "auth/login.html",
                form=form,
                fill=fill,
                msg="Invalid username or password",
                msg_type="error",
            )
        else:
            return render_template(
                "auth/login.html",
                form=form,
                fill=fill,
                msg="Invalid username or password, tries left: "
                + str(AppSettings().get("auth_tries") - failed_tries),
                msg_type="error",
            )
    else:
        return internal_server_error()


@auth.route("/logout", methods=["GET"])
def logout():
    if request.method == "GET":
        resp = make_response(redirect("/login"))
        resp.set_cookie("Authorization", "", expires=0)
        return resp
    else:
        return internal_server_error()


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)
    if request.method == "GET":
        return render_template("auth/register.html", form=form)
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            if UserService().does_user_exist(username):
                return render_template(
                    "auth/register.html",
                    form=form,
                    msg="User with provided username already exists",
                    msg_type="error",
                )
            if UserService().does_email_exist(form.email.data):
                return render_template(
                    "auth/register.html",
                    form=form,
                    msg="User with provided e-mail already exists",
                    msg_type="error",
                )

            email = form.email.data
            password = form.password1.data
            documentNumber = form.documentNumber.data

            UserService().create_user(email, username, password, documentNumber)
            return redirect("/login")

        else:
            return render_template(
                "auth/register.html",
                form=form,
                msg="Invalid data, fix form and try again",
                msg_type="error",
            )
    else:
        return internal_server_error()


@auth.route("/password_restore", methods=["GET", "POST"])
def restore_password():
    form = PasswordRestoreRequestForm(request.form)
    if request.method == "GET":
        return render_template(
            "password_restore/password_restore_request.html", form=form
        )
    if request.method == "POST":
        if form.validate():
            email = form.email.data
            if UserService().does_email_exist(email):
                user_id = UserService().get_user_id_by_email(email)
                link = (
                    current_app.config["DNS_NAME"]
                    + "/password_restore/"
                    + PasswordRestoreService().new_restore_link(user_id)
                )
                MailService().send_password_restore_mail(email, link)
            else:
                return render_template(
                    "password_restore/password_restore_request.html",
                    form=form,
                    msg="User with provided e-mail does not exist",
                    msg_type="error",
                )
            return render_template(
                "password_restore/password_restore_success.html", email=email
            )
    return render_template("password_restore/password_restore_request.html", form=form)


@auth.route("/password_restore/<string:restore_link>", methods=["GET"])
def restore_password_link(restore_link):
    user_id = PasswordRestoreService().get_user_id_by_restore_link(restore_link)
    if request.method == "GET" and user_id:
        password = PasswordRestoreService().use_restore_link(restore_link)
        UserService().change_password(user_id, password)
        return render_template(
            "password_restore/password_restored.html", password=password
        )
    return page_not_found(None)
