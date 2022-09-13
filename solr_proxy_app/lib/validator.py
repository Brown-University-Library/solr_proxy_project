import logging


log = logging.getLogger(__name__)


def check_core( core: str ) -> tuple[ bool, bool]:
    err: bool = True
    validity: bool = False
    log.debug( f'err, ``{err}``; validity, ``{validity}``' )
    return( err, validity )
    validity_dict = {
        'iip': [
            key_a, key_b,
        ]
    }