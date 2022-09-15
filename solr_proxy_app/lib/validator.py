import json, logging, pprint
from urllib.parse import ParseResult  # for type-checking
from urllib.parse import parse_qs, urlencode, urlparse 

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


# def get_parts( url: str ) -> dict[ str, str ]:
#     """ Separates the root url and the param-string. """
#     log.debug( f'url, ``{url}``' )
#     parsed_parts: ParseResult = urlparse( url )
#     log.debug( f'parsed_parts, ``{pprint.pformat(parsed_parts)}``' )
#     main: str = '%s://%s%s' % ( parsed_parts.scheme, parsed_parts.netloc, parsed_parts.path )
#     param_string: str = f'{parsed_parts.query}'
#     parts = { 'main': main, 'param_string': param_string }
#     log.debug( f'parts, ``{pprint.pformat(parts)}``' )
#     return parts


def get_legit_params( code: str, param_string: str ) -> dict:
    """ Takes given params, returns dict of legit params. """
    log.debug( f'code, ``{code}``; param_string, ``{param_string}``' )
    ## get permitted keys
    legit_keys = settings_app.LEGIT_PARAMS[code]['allowed_fields']
    log.debug( f'legit_keys, ``{legit_keys}``' )
    ## get incoming params
    parts: dict[str, list[str]] = parse_qs( param_string )
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


#     Expression of type "dict[str, list[str]]" cannot be assigned to declared type "int"
#   "dict[str, list[str]]" is incompatible with "int"