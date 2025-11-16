from .base import *

env = environ.Env()

# print(f"{BASE_DIR}/.env")
# 아래와 같이 넣어도 되지만, 실수할 수 있어 권장하지는 않음. os.path.join 써라
# environ.Env.read_env(f"{BASE_DIR}/.env")

# 2개의 경로를 합칠거야. BASE_DIR와 .env를 합칠거야. 같은결과가 출력돼고, 좀 더 안전한 느낌이야.
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
