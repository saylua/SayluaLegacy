from flask import render_template, redirect, g
from saylua.utils import is_devserver


def home():
    if g.user or is_devserver():
        return redirect('/news/', code=302)
    return render_template("landing.html")


def news():
    return render_template("news.html")