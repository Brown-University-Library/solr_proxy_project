import logging


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
    temp_return = {
        'main': 'foo', 'param_string': 'bar'
    }
    return temp_return