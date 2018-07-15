from flask import Flask, session, redirect, url_for
from functools import wraps
from scripts.database import database, User

# Wrapper for pages that require special permissions
def require_permissions(*allowed):
    def check_permissions(fn):
        @wraps(fn)
        def wrapped(**args):
            if "permissions" in session and session["permissions"] in allowed:
                return fn(**args)
            else:
                return redirect(url_for("route_login"))
        return wrapped
    return check_permissions

def login(username, password):
    session = database.session()
    user = session.query(User).filter(User.username == username, User.password == password).all()
    session.close()
    return user[0] if user else False
