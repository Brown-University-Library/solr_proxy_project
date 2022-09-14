import json, os


LEGIT_CORES = json.loads( os.environ['SOLR_PROXY__LEGIT_CORES_JSON'] )
