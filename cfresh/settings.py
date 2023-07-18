from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = 'django-insecure-+#sj*h000#4=yfdx6csq42=akhd8&5$=dfzznuszv$^+uhyua1'


DEBUG = True

ALLOWED_HOSTS = []




INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'fcm_django',
    'corsheaders',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'ckeditor',

    'users',
    'customers',
    'franchise',
    'managers',
    'products',
    'web',
    'delivery',
    'notifications',
    'orders',
    'promotions',


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173"
]

ROOT_URLCONF = 'cfresh.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cfresh.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cfresh1',
        'USER': 'TEGRAND',
        'PASSWORD': '11aa',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}



AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]




LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True



STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static"
]


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

AUTH_USER_MODEL  = 'users.User'
AUTH_PROFILE_MODULE = 'users.User'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.hostinger.com'
EMAIL_USE_SSL = True
EMAIL_PORT = 465
EMAIL_HOST_USER = 'demo@tegrand.in'
EMAIL_HOST_PASSWORD = 'Haveitnow@123'

FCM_SERVER_KEY = "AAAAcrTCfWA:APA91bE7JubpuwD4_7dDz1wSyc-uS8NWQ9y4tzoIUkXB_8kGBVqM91UqdSWgTn7QghdzJW_ReUUhkEe2EKliuteZFVCxQHeN0EvmoT83DqhTWhzqavqmqlXepqRWYaXehkfze6OvYau5"
MAP_API = "AIzaSyAKURIT9w8ziipND2CR2nNseDfv-SD7HPU"
MSG91_SENDER_ID = 'mcfrsh'
MSG91_AUTH_KEY = '337479AxWaIQVVWn5f23a0bfP1'
MSG91_DLT_TE_ID = '1307165446020474549'

