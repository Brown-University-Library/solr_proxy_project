import json, logging

from django.conf import settings as project_settings
# from django.test import TestCase
from django.test import SimpleTestCase as TestCase  # TestCase requires db
from django.test.utils import override_settings
from solr_proxy_app.lib import validator


log = logging.getLogger(__name__)
TestCase.maxDiff = 1000


class ValidateParamsTest( TestCase ):
    """ Checks param-validation. """

    def test_params__good_query( self ):
        url = 'http://127.0.0.1:9999/solr/code/select?start=0&rows=6000&indent=on&fl=inscription_id,region,city,city_geo,notBefore,notAfter,placeMenu,type,physical_type,language,language_display,religion,material&wt=json&group=true&group.field=city_pleiades&group.limit=-1&q=*:*&facet=on&facet.field=type'
        ##
        expected_main = 'http://127.0.0.1:9999/solr/code/select'
        expected_param_string = 'start=0&rows=6000&indent=on&fl=inscription_id,region,city,city_geo,notBefore,notAfter,placeMenu,type,physical_type,language,language_display,religion,material&wt=json&group=true&group.field=city_pleiades&group.limit=-1&q=*:*&facet=on&facet.field=type'
        parts: dict = validator.get_parts( url )
        self.assertEqual( expected_main, parts['main'] )
        self.assertEqual( expected_param_string, parts['param_string'] )
        ##
        expected_legit_keys = [
            'facet.field',
            'facet',
            'fl',
            'group.field',
            'group.limit',
            'group',
            'indent',
            'q',
            'rows',
            'start',
            'wt'
        ]
        expected_legit_params = {
            'facet.field': 'type',
            'facet': 'on',
            'fl': 'inscription_id,region,city,city_geo,notBefore,notAfter,placeMenu,type,physical_type,language,language_display,religion,material',
            'group.field': 'city_pleiades',
            'group.limit': '1',
            'group': 'true',
            'indent': 'on',
            'q': '*:*',
            'rows': '6000',
            'start': '0',
            'wt': 'json'
        }
        legit_params: dict = validator.get_legit_params( parts['param_string'] )
        self.assertEqual( expected_legit_keys, list(legitlegit_params_keys_and_vals.keys()) )
        self.assertEqual( expected_legit_params, legit_params )
        ##
        expected_cleaned_solr_url = 'http://127.0.0.1:9999/solr/code/select?foo=bar&foo2=bar2'
        cleaned_solr_url = validator.create_cleaned_url( expected_main, expected_legit_params  )
        self.assertEqual( expected_cleaned_solr_url, cleaned_solr_url )

    def test_params__disallow_delete( self ):
        url = 'http://127.0.0.1:9999/solr/code/select?commit=true&stream.body=<delete><query>inscription_id%3A+squf0001</query></delete>'
        ##
        expected_main = 'http://127.0.0.1:9999/solr/code/select'
        expected_param_string = 'commit=true&stream.body=<delete><query>inscription_id%3A+squf0001</query></delete>'
        parts: dict = validator.get_parts( url )
        self.assertEqual( expected_main, parts['main'] )
        self.assertEqual( expected_param_string, parts['param_string'] )
        ##
        expected_legit_keys = []
        expected_legit_params = {}
        legit_params: dict = validator.get_legit_params( parts['param_string'] )
        self.assertEqual( expected_legit_keys, list(legitlegit_params_keys_and_vals.keys()) )
        self.assertEqual( expected_legit_params, legit_params )
        ##
        expected_cleaned_solr_url = 'http://127.0.0.1:9999/solr/code/select'
        cleaned_solr_url = validator.create_cleaned_url( expected_main, expected_legit_params  )
        self.assertEqual( expected_cleaned_solr_url, cleaned_solr_url )


class ClientErrorCheckTest( TestCase ):
    """ Checks urls via test-client. """

    @override_settings(DEBUG=True)  # for tests, DEBUG autosets to False
    def test_dev_errorcheck(self):
        """ Checks that dev error_check url triggers error.. """
        log.debug( f'debug, ``{project_settings.DEBUG}``' )
        try:
            log.debug( 'about to initiate client.get()' )
            response = self.client.get( '/error_check/' )
        except Exception as e:
            log.debug( f'e, ``{repr(e)}``' )
            self.assertEqual( "Exception('Raising intentional exception.')", repr(e) )

    def test_prod_errorcheck(self):
        """ Checks that production error_check url returns 404. """
        log.debug( f'debug, ``{project_settings.DEBUG}``' )
        response = self.client.get( '/error_check/' )
        self.assertEqual( 404, response.status_code )
