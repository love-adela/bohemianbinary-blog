from .common import *   # noqa: F401,F403

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# FIXME: default file path를 적절하게 바꾸어야 합니다!

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': '/Users/adela/workspace/blog_conf/my.cnf',
        },
    }
}
