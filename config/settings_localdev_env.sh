#!/bin/bash


## LOCALDEV settings for django `x_project`
##
## This file is loaded by `env/bin/activate` when running locally...
## ...and by `project/config/passenger_wsgi.py` on our servers.
##
## When deploying on our servers, copy this file to the appropriate place, edit it, 
## ...and point to it from activate and the apache <Location> entry.


## ============================================================================
## standard project-level settings
## ============================================================================

export SOLR_PUB__SECRET_KEY="example_secret_key"

export SOLR_PUB__DEBUG_JSON="true"

export SOLR_PUB__ADMINS_JSON='
    [
      [
        "exampleFirst exampleLast",
        "example@domain.edu"
      ]
    ]
    '

export SOLR_PUB__ALLOWED_HOSTS_JSON='["127.0.0.1", "127.0.0.1:8000", "0.0.0.0:8000", "localhost:8000"]'  # must be json

export SOLR_PUB__DATABASES_JSON='
    {
      "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "HOST": "",
        "NAME": "../DB/x_project_files.sqlite3",
        "PASSWORD": "",
        "PORT": "",
        "USER": ""
      }
    }
    '

export SOLR_PUB__STATIC_URL="/static/"
export SOLR_PUB__STATIC_ROOT="/static/"

export SOLR_PUB__EMAIL_HOST="localhost"
export SOLR_PUB__EMAIL_PORT="1026"  # will be converted to int in settings.py
export SOLR_PUB__SERVER_EMAIL="donotreply_x-project@domain.edu"

export SOLR_PUB__LOG_PATH="../logs/x_project.log"
export SOLR_PUB__LOG_LEVEL="DEBUG"

export SOLR_PUB__CSRF_TRUSTED_ORIGINS_JSON='["localhost", "127.0.0.1"]'

## https://docs.djangoproject.com/en/1.11/topics/cache/
## - TIMEOUT is in seconds (0 means don't cache); CULL_FREQUENCY defaults to one-third
export SOLR_PUB__CACHES_JSON='
{
  "default": {
    "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
    "LOCATION": "../cache_dir",
    "TIMEOUT": 0,
    "OPTIONS": {
        "MAX_ENTRIES": 1000
    }
  }
}
'

## ============================================================================
## app
## ============================================================================

export SOLR_PUB__README_URL="https://github.com/birkin/django_template_32_project/blob/main/README.md"

## auth -------------------------------------------------------------

export SOLR_PUB__SUPER_USERS_JSON='[
]'

export SOLR_PUB__STAFF_USERS_JSON='
[
  "eppn@domain.edu"
]'

export SOLR_PUB__STAFF_GROUPER_GROUP="the:group"

export SOLR_PUB__TEST_META_DCT_JSON='{
  "Shibboleth-eppn": "eppn@brown.edu",
  "Shibboleth-brownNetId": "First_Last",
  "Shibboleth-mail": "first_last@domain.edu",
  "Shibboleth-givenName": "First",
  "Shibboleth-sn": "Last",
  "Shibboleth-isMemberOf": "aa:bb:cc;dd:ee:ff;the:group;gg:hh"
}'

export SOLR_PUB__LOGIN_PROBLEM_EMAIL="x_project_problems@domain.edu"


## end --------------------------------------------------------------
