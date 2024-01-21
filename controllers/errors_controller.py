from flask import Blueprint, render_template

err_handler = Blueprint("err_handler", __name__, template_folder="templates")


@err_handler.app_errorhandler(500)
def internal_server_error(e):
    return render_template("error_handling/500.html"), 500


@err_handler.app_errorhandler(404)
def page_not_found(e):
    return render_template("error_handling/404.html"), 404


@err_handler.app_errorhandler(403)
def forbidden(e):
    return render_template("error_handling/403.html"), 403


@err_handler.app_errorhandler(401)
def unauthorized(e):
    return render_template("error_handling/401.html"), 401


@err_handler.app_errorhandler(400)
def bad_request(e):
    return render_template("error_handling/400.html"), 400
