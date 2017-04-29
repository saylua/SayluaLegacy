from saylua import app
from saylua.utils import pluralize, saylua_time

from flask_markdown import Markdown

import datetime


# Attach Flask Markdown to our app.
Markdown(app, auto_reset=True, extensions=["linkify"])


@app.template_filter('pluralize')
def saylua_pluralize(count, singular_noun, plural_noun=None):
    return pluralize(count, singular_noun, plural_noun)


# Convert key to urlsafe string
@app.template_filter('make_urlsafe')
def saylua_make_urlsafe(key):
    return key.urlsafe()


# Time filters
@app.template_filter('show_date')
def saylua_show_date(time):
    time = saylua_time(time)
    return time.strftime('%b %d, %Y')


@app.template_filter('show_time')
def saylua_show_time(time):
    time = saylua_time(time)
    return time.strftime('%I:%M:%S %p SMT')


@app.template_filter('show_datetime')
def saylua_show_datetime(time):
    time = saylua_time(time)
    return time.strftime('%b %d, %Y %I:%M %p SMT')


@app.template_filter('expanded_relative_time')
def saylua_expanded_relative_time(d):
    diff = datetime.datetime.now() - d
    result = saylua_show_datetime(d)
    if diff.days >= 0 and diff.days <= 7:
        result += ' (' + saylua_relative_time(d) + ')'
    return result


# TODO Fix problem with database time not matching datetime.datetime
@app.template_filter('relative_time')
def saylua_relative_time(d):
    diff = datetime.datetime.now() - d
    s = diff.seconds
    if diff.days > 7 or diff.days < 0:
        return saylua_show_datetime(d)
    elif diff.days == 1:
        return '1 day ago'
    elif diff.days > 1:
        return '{} days ago'.format(diff.days)
    elif s <= 1:
        return 'just now'
    elif s < 60:
        return '{} seconds ago'.format(s)
    elif s < 120:
        return '1 minute ago'
    elif s < 3600:
        return '{} minutes ago'.format(s / 60)
    elif s < 7200:
        return '1 hour ago'
    else:
        return '{} hours ago'.format(s / 3600)
