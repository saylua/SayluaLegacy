from saylua import app, db

from saylua.modules.users.models.db import LoginSession
from saylua.wrappers import login_required

from ..forms.login import LoginForm, login_check

from flask import (render_template, make_response, request, redirect, flash,
    g, url_for, abort)

import datetime


@app.context_processor
def inject_sidebar_login_form():
    try:
        if g.logged_in:
            return {}
    except AttributeError:
        g.logged_in = False

    form = LoginForm()
    return dict(sidebar_form=form)


# Login form shown to the user
def login():
    form = LoginForm(request.form)

    if form.validate_on_submit():
        found = login_check.user
        found_id = found.id

        # Add a session to the datastore
        expires = datetime.datetime.utcnow()
        expires += datetime.timedelta(days=app.config['COOKIE_DURATION'])
        new_session = LoginSession(user_id=found_id, expires=expires)

        # In case there is a session id collision, merge the session entries.
        db.session.merge(new_session)
        db.session.commit()

        # Generate a matching cookie and redirect.
        resp = make_response(form.redirect())
        resp.set_cookie("session_id", new_session.id, expires=expires)
        resp.set_cookie("user_id", str(found_id), expires=expires)

        return resp

    return render_template('login/login.html', form=form)


@login_required(error="You must be logged in before you can logout.")
def logout():
    session_id = request.cookies.get('session_id')
    session = (
        db.session.query(LoginSession)
        .filter(LoginSession.id == session_id)
        .first()
    )

    # Make sure people can't log each other out
    if not session or session.user_id != g.user.id:
        abort(403)

    if session:
        db.session.delete(session)
        db.session.commit()

    resp = make_response(redirect(url_for('general.home')))
    resp.set_cookie('session_id', '', expires=0)
    flash("Bye bye! We hope to see you again soon.")
    return resp
