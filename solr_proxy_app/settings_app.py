import json, os


LEGIT_PARAMS = json.loads( os.environ['SOLR_PROXY__LEGIT_SOLR_PARAMS_JSON'] )
