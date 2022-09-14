import json, logging, pprint
from urllib.parse import ParseResult  # for type-checking
from urllib.parse import urlparse

from solr_proxy_app import settings_app


log = logging.getLogger(__name__)


def check_core( core: str ) -> bool:
    """ Checks the core-code. """
    log.debug( f'core, ``{core}``' )
    is_valid = False
    if core in settings_app.LEGIT_CORES:
        is_valid = True
    log.debug( f'is_valid, ``{is_valid}``' )
    return is_valid


def get_parts( url: str ) -> dict[ str, str ]:
    """ Separates the root url and the param-string. """
    parsed_parts: ParseResult = urlparse( url )
    log.debug( f'parsed_parts, ``{pprint.pformat(parsed_parts)}``' )
    main: str = '%s://%s%s' % ( parsed_parts.scheme, parsed_parts.netloc, parsed_parts.path )
    param_string: str = f'{parsed_parts.query}'
    parts = { 'main': main, 'param_string': param_string }
    log.debug( f'parts, ``{pprint.pformat(parts)}``' )
    return parts


# def get_legit_params(  )