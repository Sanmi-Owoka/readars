from .base import *

up.uses_netloc.append("postgres")
url = up.urlparse(env("DATABASE_URL"))

DATABASES = {
    'default': env.db("DATABASE_URL")
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True