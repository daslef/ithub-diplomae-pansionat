from collections import OrderedDict
from os import environ, path
from pathlib import Path

from django.core.management.utils import get_random_secret_key
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from unfold.contrib.constance.settings import UNFOLD_CONSTANCE_ADDITIONAL_FIELDS

######################################################################
# General
######################################################################
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = environ.get("SECRET_KEY", get_random_secret_key())

DEBUG = True

ROOT_URLCONF = "formula.urls"

WSGI_APPLICATION = "formula.wsgi.application"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10_000

######################################################################
# Domains
######################################################################
ALLOWED_HOSTS = environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

CSRF_TRUSTED_ORIGINS = environ.get(
    "CSRF_TRUSTED_ORIGINS", "http://localhost:8000,http://127.0.0.1:8000"
).split(",")

######################################################################
# Apps
######################################################################
INSTALLED_APPS = [
    "modeltranslation",
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.constance",
    "unfold.contrib.import_export",
    "unfold.contrib.guardian",
    "unfold.contrib.simple_history",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.humanize",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "debug_toolbar",
    "crispy_forms",
    "import_export",
    "guardian",
    "constance",
    "simple_history",
    "djmoney",
    "djangoql",
    "formula",
]

######################################################################
# Middleware
######################################################################
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.LoginRequiredMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
    "formula.middleware.ReadonlyExceptionHandlerMiddleware",
]

######################################################################
# Sessions
######################################################################
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

######################################################################
# Templates
######################################################################
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            path.normpath(path.join(BASE_DIR, "formula/templates")),
        ],
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

######################################################################
# Databases
######################################################################
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "database.sqlite",
    },
}

######################################################################
# Authentication
######################################################################
AUTH_USER_MODEL = "formula.User"

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
)

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

LOGIN_URL = "admin:login"

LOGIN_REDIRECT_URL = reverse_lazy("admin:index")

######################################################################
# Localization
######################################################################
LANGUAGE_CODE = "en"

TIME_ZONE = "Europe/Bratislava"

USE_I18N = True

USE_TZ = True

LANGUAGES = (
    ("de", _("German")),
    ("en", _("English")),
)

# https://docs.djangoproject.com/en/5.1/ref/settings/#date-input-formats
DATE_INPUT_FORMATS = [
    "%d.%m.%Y",  # Custom input
    "%Y-%m-%d",  # '2006-10-25'
    "%m/%d/%Y",  # '10/25/2006'
    "%m/%d/%y",  # '10/25/06'
    "%b %d %Y",  # 'Oct 25 2006'
    "%b %d, %Y",  # 'Oct 25, 2006'
    "%d %b %Y",  # '25 Oct 2006'
    "%d %b, %Y",  # '25 Oct, 2006'
    "%B %d %Y",  # 'October 25 2006'
    "%B %d, %Y",  # 'October 25, 2006'
    "%d %B %Y",  # '25 October 2006'
    "%d %B, %Y",  # '25 October, 2006'
]

# https://docs.djangoproject.com/en/5.1/ref/settings/#datetime-input-formats
DATETIME_INPUT_FORMATS = [
    "%d.%m.%Y %H:%M:%S",  # Custom input
    "%Y-%m-%d %H:%M:%S",  # '2006-10-25 14:30:59'
    "%Y-%m-%d %H:%M:%S.%f",  # '2006-10-25 14:30:59.000200'
    "%Y-%m-%d %H:%M",  # '2006-10-25 14:30'
    "%m/%d/%Y %H:%M:%S",  # '10/25/2006 14:30:59'
    "%m/%d/%Y %H:%M:%S.%f",  # '10/25/2006 14:30:59.000200'
    "%m/%d/%Y %H:%M",  # '10/25/2006 14:30'
    "%m/%d/%y %H:%M:%S",  # '10/25/06 14:30:59'
    "%m/%d/%y %H:%M:%S.%f",  # '10/25/06 14:30:59.000200'
    "%m/%d/%y %H:%M",  # '10/25/06 14:30'
]

######################################################################
# Static
######################################################################
STATIC_URL = "/static/"

STATICFILES_DIRS = [BASE_DIR / "formula" / "static"]

STATIC_ROOT = BASE_DIR / "static"

MEDIA_ROOT = BASE_DIR / "media"

MEDIA_URL = "/media/"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

######################################################################
# Unfold
######################################################################
UNFOLD = {
    "SITE_TITLE": _("Formula Admin"),
    "SITE_HEADER": _("Formula Admin"),
    "SITE_SUBHEADER": _("Unfold demo project"),
    "SITE_SYMBOL": "dashboard",
    "SITE_ICON": lambda request: static("formula/images/logo.svg"),
    # "SITE_URL": None,
    # "SHOW_HISTORY": True,
    "SHOW_LANGUAGES": True,
    "LANGUAGE_FLAGS": {
        "de": "🇩🇪",
        "en": "🇺🇸",
    },
    "ENVIRONMENT": "formula.utils.environment_callback",
    # "DASHBOARD_CALLBACK": "formula.views.dashboard_callback",
    "LOGIN": {
        "image": lambda request: static("formula/images/login-bg.jpg"),
        "form": "formula.forms.LoginForm",
    },
    "STYLES": [
        # lambda request: static("css/styles.css"),
    ],
    "SCRIPTS": [
        # lambda request: static("js/chart.min.js"),
    ],
    "TABS": [
        {
            "models": [
                "formula.race",
                "formula.constructor",
            ],
            "items": [
                {
                    "title": _("Races"),
                    "link": reverse_lazy("admin:formula_race_changelist"),
                },
                {
                    "title": _("Constructors"),
                    "link": reverse_lazy("admin:formula_constructor_changelist"),
                },
            ],
        },
        {
            "page": "drivers",
            "models": ["formula.driver"],
            "items": [
                {
                    "title": _("Drivers"),
                    "link": reverse_lazy("admin:formula_driver_changelist"),
                    "active": lambda request: request.path
                    == reverse_lazy("admin:formula_driver_changelist")
                    and "status__exact" not in request.GET,
                },
                {
                    "title": _("Active drivers"),
                    "link": lambda request: f"{
                        reverse_lazy('admin:formula_driver_changelist')
                    }?status__exact=ACTIVE",
                },
                {
                    "title": _("Crispy Form"),
                    "link": reverse_lazy("admin:crispy_form"),
                },
                {
                    "title": _("Crispy Formset"),
                    "link": reverse_lazy("admin:crispy_formset"),
                },
            ],
        },
    ],
    # "COMMAND": {
    #     "search_models": "formula.utils.search_models_callback",
    #     "show_history": "formula.utils.show_history_callback",
    # },
    "SIDEBAR": {
        "show_search": False,
        "show_all_applications": False,
        "command_search": False,
        "navigation": [
            {
                "title": _("Navigation"),
                "items": [
                    {
                        "title": _("Drivers"),
                        "icon": "sports_motorsports",
                        "active": "formula.utils.driver_list_link_callback",
                        "link": reverse_lazy("admin:formula_driver_changelist"),
                    },
                    {
                        "title": _("Circuits"),
                        "icon": "sports_score",
                        "link": reverse_lazy("admin:formula_circuit_changelist"),
                    },
                    {
                        "title": _("Races"),
                        "icon": "stadium",
                        "link": reverse_lazy("admin:formula_race_changelist"),
                        "badge": "formula.utils.badge_callback",
                        "badge_variant": "danger",
                        "badge_style": "solid",
                    },
                    {
                        "title": _("Constance"),
                        "icon": "settings",
                        "link": reverse_lazy("admin:constance_config_changelist"),
                        "badge": _("New"),
                        "badge_variant": "primary",
                    },
                ],
            },
            {
                "title": _("Users & Groups"),
                "collapsible": True,
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "account_circle",
                        "link": reverse_lazy("admin:formula_user_changelist"),
                    },
                    {
                        "title": _("Groups"),
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                ],
            },
        ],
    },
}

######################################################################
# Money
######################################################################
CURRENCIES = ("USD", "EUR")

######################################################################
# App
######################################################################
LOGIN_USERNAME = environ.get("LOGIN_USERNAME")

LOGIN_PASSWORD = environ.get("LOGIN_PASSWORD")

############################################################################
# Debug toolbar
############################################################################
DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG}

######################################################################
# Crispy forms
######################################################################
CRISPY_TEMPLATE_PACK = "unfold_crispy"

CRISPY_ALLOWED_TEMPLATE_PACKS = ["unfold_crispy"]

######################################################################
# Constance
######################################################################
CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"

CONSTANCE_CONFIG = {
    "SITE_NAME": ("My Title", _("Website title")),
    "SITE_DESCRIPTION": ("", _("Website description")),
    "THEME": ("light-blue", _("Website theme"), "choice_field"),
    "IN_CONSTRUCTION": (False, _("Website in construction")),
    "SITE_URL": ("", _("Website URL")),
    "SITE_LOGO": ("", _("Website logo"), "image_field"),
    "SITE_FAVICON": ("", _("Website favicon"), "file_field"),
    "SITE_BACKGROUND_IMAGE": ("", _("Website background image"), "image_field"),
    "SITE_BACKGROUND_COLOR": ("#FFFFFF", _("Website background color")),
    "SITE_FONT_SIZE": (16, _("Base font size in pixels")),
    "SITE_ANALYTICS_ID": ("", _("Google Analytics ID")),
    "SITE_MAINTENANCE_MODE": (False, _("Enable maintenance mode")),
    "SITE_MAINTENANCE_MESSAGE": ("", _("Maintenance mode message")),
    "SITE_SOCIAL_LINKS": ("", _("Social media links")),
    "SITE_FOOTER_TEXT": ("", _("Footer text")),
    "SITE_META_KEYWORDS": ("", _("Meta keywords")),
    "SITE_CACHE_TTL": (3600, _("Cache TTL in seconds")),
    "SITE_DATE_FORMAT": ("%Y-%m-%d", _("Date format")),
    "SITE_TIME_ZONE": ("UTC", _("Time zone")),
}

CONSTANCE_CONFIG_FIELDSETS = OrderedDict(
    {
        "General Settings": {
            "fields": (
                "SITE_NAME",
                "SITE_DESCRIPTION",
                "SITE_URL",
            ),
            # "collapse": False,
        },
        "Theme & Design": {
            "fields": (
                "THEME",
                "SITE_FONT_SIZE",
                "SITE_BACKGROUND_COLOR",
                "SITE_BACKGROUND_IMAGE",
            ),
            # "collapse": False,
        },
        "Assets": {
            "fields": (
                "SITE_LOGO",
                "SITE_FAVICON",
            ),
            # "collapse": True,
        },
        "Content": {
            "fields": (
                "SITE_FOOTER_TEXT",
                "SITE_META_KEYWORDS",
                "SITE_SOCIAL_LINKS",
            ),
            # "collapse": True,
        },
        "System": {
            "fields": (
                "IN_CONSTRUCTION",
                "SITE_MAINTENANCE_MODE",
                "SITE_MAINTENANCE_MESSAGE",
                "SITE_CACHE_TTL",
                "SITE_DATE_FORMAT",
                "SITE_TIME_ZONE",
                "SITE_ANALYTICS_ID",
            ),
            # "collapse": True,
        },
    }
)


CONSTANCE_ADDITIONAL_FIELDS = {
    **UNFOLD_CONSTANCE_ADDITIONAL_FIELDS,
    "choice_field": [
        "django.forms.fields.ChoiceField",
        {
            "widget": "unfold.widgets.UnfoldAdminSelectWidget",
            "choices": (
                ("light-blue", "Light blue"),
                ("dark-blue", "Dark blue"),
            ),
        },
    ],
}
