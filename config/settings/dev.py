from .base import *

up.uses_netloc.append("postgres")
url = up.urlparse(env("DATABASE_URL"))

DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'), conn_max_age=600)
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True