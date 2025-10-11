from django.urls import reverse_lazy
from pathlib import Path
import os
import environ
from django.contrib.messages import constants as messages

env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

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

ALLOWED_HOSTS = []


# Application definition

SYSTEM_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "bootstrap4",
    "rest_framework",
    "rest_framework.authtoken",
    "requests",
    "openpyxl",
]

CUSTOM_APPS = [
    "common.apps.CommonConfig",
    "users.apps.UsersConfig",
    "articles.apps.ArticlesConfig",
    "core.apps.CoreConfig",
    "categories.apps.CategoriesConfig",
    "rooms.apps.RoomsConfig",
    "blogs.apps.BlogsConfig",
    "comments.apps.CommentsConfig",
    "news.apps.NewsConfig",
    "polls.apps.PollsConfig",
    "profiles.apps.ProfilesConfig",
    "projects.apps.ProjectsConfig",
    "search.apps.SearchConfig",
    "videos.apps.VideosConfig",
    "likes.apps.LikesConfig",
]


INSTALLED_APPS = SYSTEM_APPS + THIRD_PARTY_APPS + CUSTOM_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

MESSAGE_TAGS = {
    messages.ERROR: "danger",
}

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"

# STATIC_ROOT라는 변수에 우리가 python manage.py collectstatic을 했을 때 경로를 지정해준 것임
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# media 관련 설정
# MEDIA_URL은 주소창에 MEDIA 이하의 경로로 접근을 해야지 실제 MEDIA 파일에 접근가능함
# 예) 127.0.0.1:8000/MEDIA/TEST.jpg
# MEDIA_ROOT는 MEDIA 파일을 서버에 올렸을 때,어느경로에 지정이 될 것인지, 그 바닥에 있는 경로가 어디가 될것인지에 대한 정보
# 장고에서 이미지를 관리할 때 필요한 라이브러리가 있음 (pillow 설치: pip install pillow)
# 이것은 그냥 url을 위한 거야.
MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"

LOGIN_REDIRECT_URL = reverse_lazy("core:home")
LOGOUT_REDIRECT_URL = reverse_lazy("users:login")


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "config.authentication.JWTAuthentication",
    ]
}
