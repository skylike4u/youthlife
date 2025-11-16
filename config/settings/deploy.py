from .base import *

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# print(f"{BASE_DIR}/.env")
# 아래와 같이 넣어도 되지만, 실수할 수 있어 권장하지는 않음. os.path.join 써라
# environ.Env.read_env(f"{BASE_DIR}/.env")

# 2개의 경로를 합칠거야. BASE_DIR와 .env를 합칠거야. 같은결과가 출력돼고, 좀 더 안전한 느낌이야.
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debugDJANGO_SETTINGS_MODULE turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# docker에서 HOST 의 경우, 컨테이너의 이름을 통해서(도메인을 통해서) 통신을 하기때문에, mariadb의 컨테이너 이름을 여기에 적어 줘야 된다.
# mariadb의 port는 3306을 사용한다 (mysql도 동일)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "django",
        "USER": "django",
        "PASSWORD": "password1234",
        "HOST": "mariadb",
        "PORT": "3306",
    }
}
