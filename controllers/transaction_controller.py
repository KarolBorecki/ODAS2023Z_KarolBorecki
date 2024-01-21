from flask import Blueprint, render_template, request
from controllers.errors_controller import unauthorized
from controllers.forms.new_transaction_form import NewTranactionForm

from controllers.middlewares.auth_middlewares import token_required
from services.hash_service import HashService
from services.transaction_service import TransactionService
from services.user_service import UserService

transactions = Blueprint("transactions", __name__, template_folder="templates")


@transactions.route("/transactions", methods=["GET"])
@token_required
def transactions_list(current_user):
    incomes = TransactionService().get_incomes(current_user.user_id)
    expenses = TransactionService().get_expenses(current_user.user_id)
    incomes = [
        dict(
            income,
            **{
                "type": "income",
                "other_client_nr": UserService().get_user_client_nr(income["from_id"]),
            }
        )
        for income in incomes
    ]
    expenses = [
        dict(
            expense,
            **{
                "type": "expense",
                "other_client_nr": UserService().get_user_client_nr(expense["to_id"]),
            }
        )
        for expense in expenses
    ]
    transactions = incomes + expenses
    transactions.sort(key=lambda transaction: transaction["date_created"], reverse=True)
    return render_template(
        "transaction/transaction_list.html", transactions=transactions
    )


@transactions.route("/transactions/new", methods=["GET", "POST"])
@token_required
def transactions_new(current_user):
    form = NewTranactionForm(request.form)
    if request.method == "GET":
        csrf = HashService().generate_csrf_token()
        UserService().set_csrf(current_user.user_id, csrf)
        return render_template("transaction/new_transaction.html", form=form, csrf=csrf)
    elif request.method == "POST":
        got_csrf = request.form['csrf-token']
        if got_csrf != UserService().get_csrf(current_user.user_id):
            return unauthorized(None)
        
        if form.validate():
            to_id = UserService().get_user_id_by_client_nr(form.to.data)
            from_id = current_user.user_id
            if to_id and to_id != from_id:
                TransactionService().new(
                    form.title.data, from_id, to_id, form.value.data
                )
                return render_template(
                    "transaction/new_transaction.html",
                    form=form,
                    csrf=got_csrf,
                    msg="Transaction created.",
                    msg_type="success",
                )
            else:
                return render_template(
                    "transaction/new_transaction.html",
                    form=form,
                    csrf=got_csrf,
                    msg="Invalid client number.",
                    msg_type="error",
                )
        else:
            return render_template(
                "transaction/new_transaction.html",
                form=form,
                csrf=got_csrf,
                msg="Provided invalid data.",
                msg_type="error",
            )

    return unauthorized(None)
