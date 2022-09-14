#!/bin/bash


## LOCALDEV settings for django `solr_proxy_project`
##
## This file is loaded by `env/bin/activate` when running locally...
## ...and by `project/config/passenger_wsgi.py` on our servers.
##
## When deploying on our servers, copy this file to the appropriate place, edit it, 
## ...and point to it from activate and the apache <Location> entry.


## ============================================================================
## standard project-level settings
## ============================================================================

export SOLR_PROXY__SECRET_KEY="example_secret_key"

export SOLR_PROXY__DEBUG_JSON="true"

export SOLR_PROXY__ADMINS_JSON='
    [
      [
        "exampleFirst exampleLast",
        "example@domain.edu"
      ]
    ]
    '

export SOLR_PROXY__ALLOWED_HOSTS_JSON='["127.0.0.1", "127.0.0.1:8000", "0.0.0.0:8000", "localhost:8000"]'  # must be json

# export SOLR_PROXY__DATABASES_JSON='  # disabled; no DB in initial release
#     {
#       "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "HOST": "",
#         "NAME": "../DB/solr_proxy_project_files.sqlite3",
#         "PASSWORD": "",
#         "PORT": "",
#         "USER": ""
#       }
#     }
#     '

export SOLR_PROXY__STATIC_URL="/static/"
export SOLR_PROXY__STATIC_ROOT="/static/"

export SOLR_PROXY__EMAIL_HOST="localhost"
export SOLR_PROXY__EMAIL_PORT="1026"  # will be converted to int in settings.py
export SOLR_PROXY__SERVER_EMAIL="donotreply_x-project@domain.edu"

export SOLR_PROXY__LOG_PATH="../logs/solr_proxy_project.log"
export SOLR_PROXY__LOG_LEVEL="DEBUG"

export SOLR_PROXY__CSRF_TRUSTED_ORIGINS_JSON='["localhost", "127.0.0.1"]'

## https://docs.djangoproject.com/en/1.11/topics/cache/
## - TIMEOUT is in seconds (0 means don't cache); CULL_FREQUENCY defaults to one-third
export SOLR_PROXY__CACHES_JSON='
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

export SOLR_PROXY__LEGIT_CORES_JSON='
[
  "aa",
  "bb"
]
'

# export SOLR_PROXY__README_URL="https://github.com/birkin/solr_proxy_project/blob/main/README.md"

## auth -------------------------------------------------------------

# export SOLR_PROXY__SUPER_USERS_JSON='[
# ]'

# export SOLR_PROXY__STAFF_USERS_JSON='
# [
#   "eppn@domain.edu"
# ]'

# export SOLR_PROXY__STAFF_GROUPER_GROUP="the:group"

# export SOLR_PROXY__TEST_META_DCT_JSON='{
#   "Shibboleth-eppn": "eppn@brown.edu",
#   "Shibboleth-brownNetId": "First_Last",
#   "Shibboleth-mail": "first_last@domain.edu",
#   "Shibboleth-givenName": "First",
#   "Shibboleth-sn": "Last",
#   "Shibboleth-isMemberOf": "aa:bb:cc;dd:ee:ff;the:group;gg:hh"
# }'

# export SOLR_PROXY__LOGIN_PROBLEM_EMAIL="solr_proxy_project_problems@domain.edu"


## end --------------------------------------------------------------
