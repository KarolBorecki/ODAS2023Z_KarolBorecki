from flask import Blueprint, render_template, request
from controllers.errors_controller import internal_server_error, unauthorized
from controllers.forms.edit_account_form import EditAccountForm
from controllers.forms.number_request_form import NumberRequestForm

from controllers.middlewares.auth_middlewares import token_required
from services.hash_service import HashService
from services.repositories.tries_repository import TriesRepository
from services.user_service import UserService

account = Blueprint("account", __name__, template_folder="templates")


@account.route("/account", methods=["GET", "POST"])
@token_required
def account_info(current_user):
    current_user.client_nr = UserService().get_user_client_nr(current_user.user_id)
    current_user.email = UserService().get_user_email(current_user.user_id)
    if request.method == "GET":
        current_user.document_number = UserService().get_user_hidden_document(
            current_user.user_id
        )
        return render_template("account/account_info.html", user=current_user)
    if request.method == "POST":
        form = NumberRequestForm(request.form)
        password = form.password.data
        if UserService().verify_password(current_user.user_id, password):
            document_number = UserService().get_user_document(current_user.user_id)
            print(document_number)
            current_user.document_number = document_number
            current_user.is_document_number_visible = True
            return render_template(
                "account/account_info.html",
                user=current_user,
                msg="Document number request successfully",
                msg_type="success",
            )
        else:
            return render_template(
                "account/account_info.html",
                user=current_user,
                msg="Invalid credentials",
                msg_type="error",
            )
    else:
        return render_template("account/account_info.html", user=current_user)


@account.route("/account/history", methods=["GET"])
@token_required
def account_history(current_user):
    logging_list = TriesRepository().get("user_id", current_user.user_id)
    logging_list = sorted(logging_list, key=lambda k: k["date"], reverse=True)
    for logging in logging_list:
        logging.pop("id", None)
        logging.pop("user_id", None)
    return render_template(
        "account/account_login_history.html", logging_list=logging_list
    )


@account.route("/account/edit", methods=["GET", "POST"])
@token_required
def account_edit(current_user):
    form = EditAccountForm(request.form)

    if request.method == "GET":
        form.username.data = current_user.username
        email = UserService().get_user_email(current_user.user_id)
        form.email.data = email
        csrf = HashService().generate_csrf_token()
        UserService().set_csrf(current_user.user_id, csrf)
        return render_template("account/edit_account.html", form=form, csrf=csrf)
    
    elif request.method == "POST":
        got_csrf = request.form['csrf-token']
        if got_csrf != UserService().get_csrf(current_user.user_id):
            return unauthorized(None)
        
        if form.validate():
            password = form.oldPassword.data
            if UserService().verify_password(current_user.user_id, password):
                UserService().update_user(
                    current_user.user_id, form.email.data, form.username.data, form.newPassword1.data
                )
                return render_template(
                    "account/edit_account.html",
                    form=form,
                    csrf=got_csrf,
                    msg="Account updated successfully",
                    msg_type="success",
                )
            return render_template(
                "account/edit_account.html",
                form=form,
                csrf=got_csrf,
                msg="Provided credentials are invalid",
                msg_type="error",
            )
        else:
            return render_template("account/edit_account.html", form=form, csrf=got_csrf)
    else:
        return unauthorized(None)


@account.route("/account/request_number", methods=["GET", "POST"])
@token_required
def full_number_request(current_user):
    form = NumberRequestForm(request.form)
    if request.method == "GET":
        return render_template("account/number_request.html", form=form)
    else:
        return render_template("account/number_request.html", form=form)
