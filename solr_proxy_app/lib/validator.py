import logging, pprint

from urllib.parse import ParseResult  # for type-checking
from urllib.parse import urlparse


log = logging.getLogger(__name__)


def check_core( core: str ) -> tuple[ bool, bool]:
    """ Checks the core-code. """
    err: bool = True
    validity: bool = False
    log.debug( f'err, ``{err}``; validity, ``{validity}``' )
    return( err, validity )
    validity_dict = {
        'iip': [
            key_a, key_b,
        ]
    }


def get_parts( url: str ) -> dict[ str, str ]:
    """ Separates the root url and the param-string. """
    parsed_parts: ParseResult = urlparse( url )
    log.debug( f'parsed_parts, ``{pprint.pformat(parsed_parts)}``' )
    main: str = '%s://%s%s' % ( parsed_parts.scheme, parsed_parts.netloc, parsed_parts.path )
    param_string: str = f'{parsed_parts.query}'
    parts = { 'main': main, 'param_string': param_string }
    log.debug( f'parts, ``{pprint.pformat(parts)}``' )
    return parts