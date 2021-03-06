from flask import Blueprint, Flask
from flask.globals import _request_ctx_stack
from flask.helpers import send_from_directory
from flask.templating import DispatchingJinjaLoader

from collections import namedtuple
from importlib import import_module

import os.path


class SayluaApp(Flask):
    """Extends the default Flask app to attempt to locate static files from Blueprints before 404'ing."""
    def __init__(self, name):
        super(SayluaApp, self).__init__(name)
        self.jinja_options = Flask.jinja_options.copy()
        self.jinja_options['loader'] = SayluaLoader(self)

    def send_static_file(self, filename):
        for blueprint_name, blueprint in self.blueprints.items():
            filepath = os.path.join(blueprint.static_folder, filename)

            if os.path.exists(filepath):
                return send_from_directory(blueprint.static_folder, filename)

        return super(SayluaApp, self).send_static_file(filename)


class SayluaRouter(Blueprint):
    """URL Routing syntax sugar."""

    @classmethod
    def create_blueprint(cls, module_name, import_name):
        return cls(
            module_name,
            import_name,
            static_folder='static',
            template_folder='templates',
            static_url_path='/static_{}'.format(module_name),
            url_prefix=None
        )

    def register_urls(self, urls):
        for _url in urls:
            self.add_url_rule(rule=_url.rule, endpoint=_url.name, view_func=_url.view_func,
                methods=_url.methods)


class SayluaLoader(DispatchingJinjaLoader):
    """Prevent template namespace collisions between modules.
    Additionally, prefer local templates to global templates.
    This means that global templates will no longer override local templates.
    """
    def _iter_loaders(self, template):
        blueprint = _request_ctx_stack.top.request.blueprint
        if blueprint is not None and blueprint in self.app.blueprints:
            loader = self.app.blueprints[blueprint].jinja_loader
            if loader is not None:
                yield blueprint, loader

        loader = self.app.jinja_loader
        if loader is not None:
            yield self.app, loader


def url(rule, view_func, name=None, methods=["GET"]):
    """Simple URL wrapper for SayluaRouter.

    Usage:
    ```
    from . import views

    url('/adventure/', view_func=views.adventure_home, name='adventure_home', methods=['GET'])
    url('/adventure/', view_func=views.adventure_home, name='adventure_home')
    url('/adventure/', views.adventure_home, 'adventure_home')
    url('/adventure/', views.adventure_home)
    ```

    # Note that 'endpoint' is now 'name'.
    # Note also that the name and view_func parameters are reversed from that of
    a normal flask URL.
    """

    __url = namedtuple('Url', ['rule', 'name', 'view_func', 'methods'])
    return __url(rule, name, view_func, methods)


def register_urls(app, modules):
    """Don't try to understand this."""

    for module_name in modules:
        formatted_module = "saylua.modules.{}".format(module_name)
        __module = import_module(formatted_module)
        app.register_blueprint(__module.blueprint)
