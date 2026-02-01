from flask import session


def isAuthorised():
    return "currentUser" in session