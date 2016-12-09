# =======================================================
#
#  Pets -- Pet and Den pages
#  ---------------------------------
#  Pets, man. What do you want from me?
#
# =======================================================

from saylua.routing import SayluaRouter
from . import urls

MODULE_NAME = 'pets'
IMPORT_NAME = __name__

blueprint = SayluaRouter.create_blueprint(MODULE_NAME, IMPORT_NAME)
blueprint.register_urls(urls.urlpatterns)
