from . import auth
from . import groups
from . import hub
from . import notifications
from . import proxy
from . import services
from . import users
from .base import *

default_handlers = []
for mod in (auth, hub, proxy, users, groups, services, notifications):
    default_handlers.extend(mod.default_handlers)
