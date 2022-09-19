import json, logging, pprint
from urllib.parse import ParseResult  # for type-checking
from urllib.parse import parse_qs, urlencode, urlparse 

from django.http import QueryDict
from solr_proxy_app import settings_app


log = logging.getLogger(__name__)


def check_core( core: str ) -> bool:
    """ Checks the core-code. """
    log.debug( f'core, ``{core}``' )
    is_valid = False
    if core in settings_app.LEGIT_PARAMS.keys():
        is_valid = True
    log.debug( f'is_valid, ``{is_valid}``' )
    return is_valid


def get_legit_params( code: str, param_string: str ) -> dict:
    """ Takes given params, returns dict of legit params. """
    log.debug( f'code, ``{code}``; param_string, ``{param_string}``' )
    ## get permitted keys
    legit_keys = settings_app.LEGIT_PARAMS[code]['allowed_fields']
    log.debug( f'legit_keys, ``{legit_keys}``' )
    ## get incoming params
    parts: dict[str, list[str]] = parse_qs( param_string )  # parse_qs will convert foo=a&foo=b into {'foo': ['a', 'b']}
    log.debug( f'parts, ``{pprint.pformat(parts)}``' )
    ok_fields: dict = {}
    for (key, val) in parts.items():
        log.debug( f'key, ``{key}``; val, ``{val}``' )
        part_key: str = key
        part_val: list = val
        if part_key in legit_keys:
            ok_fields[part_key] = part_val
        else:
            log.warning( f'key, ``{part_key}`` not valid; (value, ``{part_val}``)' )
    log.debug( f'ok_fields, ``{pprint.pformat(ok_fields)}``' )
    return ok_fields


def create_cleaned_url( code: str, params: dict ) -> str:
    """ Takes root-url and params and returns solr url. """
    ## encode incoming params-dict
    log.debug( f'params, ``{pprint.pformat(params)}``' )
    param_string: str = urlencode( params, doseq=True, safe=',*:' )
    log.debug( f'param_string, ``{param_string}``' )
    ## get real solr url
    solr_root: str = settings_app.LEGIT_PARAMS[code]['real_solr_root']
    cleaned_url: str = f'{solr_root}?{param_string}'
    log.debug( f'cleaned_url, ``{cleaned_url}``' )
    return cleaned_url


def convert_post_params_to_querystring( code: str, qdict: QueryDict ) -> str:
    """ Takes incoming parameters (from, for example, POST-params) and returns a valid querystring. """
    log.debug( f'qdict, ``{qdict}``' )
    ## get legit keys for given code --------------------------------
    legit_keys = settings_app.LEGIT_PARAMS[code]['allowed_fields']
    ## create a mutable QueryDict we can remove keys from -----------
    qdict_stringified:str = qdict.urlencode()
    log.debug( f'qdict_stringified, ``{qdict_stringified}``' )
    new_qdict = QueryDict( qdict_stringified, mutable=True )
    ## validate keys ------------------------------------------------
    qdict_keys = qdict.keys()
    log.debug( f'qdict_keys, ``{qdict_keys}``' )
    for key in qdict_keys:
        if key not in legit_keys:
            new_qdict.pop(key)  # can't pop from the qdict we're iterating through
    log.debug( f'updated-new_qdict, ``{new_qdict}``' )
    ## convert to querystring ---------------------------------------
    new_qdict_stringified: str = new_qdict.urlencode()
    ok_string = new_qdict_stringified
    log.debug( f'ok_string, ``{ok_string}``' )
    return ok_string
