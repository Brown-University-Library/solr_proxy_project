import json, logging
from urllib.parse import ParseResult  # for type-checking
from urllib.parse import urlparse 


from django.conf import settings as project_settings
# from django.test import TestCase
from django.test import SimpleTestCase as TestCase  # TestCase requires db
from django.test.utils import override_settings
from solr_proxy_app.lib import validator
from solr_proxy_app import settings_app


log = logging.getLogger(__name__)
TestCase.maxDiff = 1000


class ValidatorTest( TestCase ):
    """ Checks param-validation. """

    def test_validate_core_code( self ):
        """ Checks validation of detected core. """
        good_core: str = list( settings_app.LEGIT_PARAMS.keys() )[0]
        self.assertEqual( True, validator.check_core(good_core) )
        self.assertEqual( False, validator.check_core('bad_core') )

    def test_params__good_query( self ):
        """ Checks parsing of good url. """
        url = 'http://127.0.0.1:9999/solr/code/select?start=0&rows=6000&indent=on&fl=inscription_id,region,city,city_geo,notBefore,notAfter,placeMenu,type,physical_type,language,language_display,religion,material&wt=json&group=true&group.field=city_pleiades&group.limit=-1&q=*:*&facet=on&facet.field=type'
        ## setup expectations ---------------------------------------
        expected_param_string = 'start=0&rows=6000&indent=on&fl=inscription_id,region,city,city_geo,notBefore,notAfter,placeMenu,type,physical_type,language,language_display,religion,material&wt=json&group=true&group.field=city_pleiades&group.limit=-1&q=*:*&facet=on&facet.field=type'
        expected_ok_keys = [
            'facet',
            'facet.field',
            'fl',
            'group',
            'group.field',
            'group.limit',
            'indent',
            'q',
            'rows',
            'start',
            'wt'
        ]
        expected_ok_params = {
            'start': ['0'], 
            'rows': ['6000'], 
            'indent': ['on'], 
            'fl': ['inscription_id,region,city,city_geo,notBefore,notAfter,placeMenu,type,physical_type,language,language_display,religion,material'], 
            'wt': ['json'], 
            'group': ['true'], 
            'group.field': ['city_pleiades'], 
            'group.limit': ['-1'], 
            'q': ['*:*'], 
            'facet': ['on'], 
            'facet.field': ['type']
        }
        ## prepare querystring --------------------------------------
        parsed_parts: ParseResult = urlparse( url )
        param_string: str = parsed_parts.query
        ## get legit_params -----------------------------------------
        legit_params: dict = validator.get_legit_params( 'iip', param_string )
        log.debug( f'legit_params, ``{legit_params}``' )
        keys: list = list( legit_params.keys() )
        log.debug( f'keys, ``{keys}``' )
        sorted_keys = sorted( keys )
        log.debug( f'sorted_keys, ``{sorted_keys}``' )
        ## params tests ---------------------------------------------
        self.assertEqual( expected_ok_keys, sorted_keys )
        self.assertEqual( expected_ok_params, legit_params )
        ## pepare cleaned_solr_url ----------------------------------
        expected_cleaned_param_string: str = expected_param_string  # in this case the original param-string, since all fields are legit.
        log.debug( f'expected_cleaned_param_string, ``{expected_cleaned_param_string}``' )
        cleaned_solr_url: str = validator.create_cleaned_url( 'iip', expected_ok_params  )
        ## test cleaned_solr_url params -----------------------------
        parsed_parts: ParseResult = urlparse( cleaned_solr_url )
        cleaned_param_string: str = parsed_parts.query
        log.debug( f'cleaned_param_string, ``{cleaned_param_string}``' )
        self.assertEqual( expected_cleaned_param_string, cleaned_param_string )

    def test_params__disallow_delete( self ):
        url = 'http://127.0.0.1:9999/solr/code/select?commit=true&stream.body=<delete><query>inscription_id%3A+squf0001</query></delete>'
        ## setup expectations ---------------------------------------
        expected_ok_keys = []
        expected_ok_params = {}
        ## prepare querystring --------------------------------------
        parsed_parts: ParseResult = urlparse( url )
        param_string: str = parsed_parts.query
        ## get legit_params -----------------------------------------
        legit_params: dict = validator.get_legit_params( 'iip', param_string )
        ## params tests ---------------------------------------------
        self.assertEqual( expected_ok_keys, list(legit_params.keys()) )
        self.assertEqual( expected_ok_params, legit_params )
        ## pepare cleaned_solr_url ----------------------------------
        expected_cleaned_param_string: str = ''  
        log.debug( f'expected_cleaned_param_string, ``{expected_cleaned_param_string}``' )
        cleaned_solr_url: str = validator.create_cleaned_url( 'iip', expected_ok_params  )
        ## test cleaned_solr_url params -----------------------------
        parsed_parts: ParseResult = urlparse( cleaned_solr_url )
        cleaned_param_string: str = parsed_parts.query
        log.debug( f'cleaned_param_string, ``{cleaned_param_string}``' )
        self.assertEqual( expected_cleaned_param_string, cleaned_param_string )

    def test_get_legit_params__simple(self):
        querystring = 'start=0&rows=6000&fl=inscription_id&foo=bar'
        ok_params: dict = validator.get_legit_params( 'iip', querystring )
        self.assertEqual( 
            {'fl': ['inscription_id'], 'rows': ['6000'], 'start': ['0']}, 
            ok_params 
            )

    def test_get_legit_params__multiple(self):
        querystring = 'facet.field=physical_type&facet.field=language&facet.field=religion&fl=inscription_id&foo=bar'
        ok_params: dict = validator.get_legit_params( 'iip', querystring )
        self.assertEqual( 
            {'facet.field': ['physical_type', 'language', 'religion'],'fl': ['inscription_id']}, 
            ok_params 
            )

    def test_convert_post_params_to_querystring__simple(self):
        from django.http import QueryDict
        qdict = QueryDict('start=0&rows=6000&fl=inscription_id&foo=bar')
        self.assertEqual( 
            'start=0&rows=6000&fl=inscription_id', 
            validator.convert_post_params_to_querystring( 'iip', qdict ) 
            )

    def test_convert_post_params_to_querystring__multiple(self):
        from django.http import QueryDict
        qdict = QueryDict('facet.field=physical_type&facet.field=language&facet.field=religion&fl=inscription_id&foo=bar')
        self.assertEqual( 
            'facet.field=physical_type&facet.field=language&facet.field=religion&fl=inscription_id', 
            validator.convert_post_params_to_querystring( 'iip', qdict ) 
            )
        
    def test_convert_post_params_to_querystring__allow_facetquery(self):
        from django.http import QueryDict
        # qdict = QueryDict('facet.field=physical_type&facet.field=language&facet.field=religion&fl=inscription_id&foo=bar')
        
        # {'start': ['0'], 'rows': ['0'], 'indent': ['on'], 'fl': ['inscription_id,region,city,city_geo,notBefore,notAfter,placeMenu,type,physical_type,language,language_display,religion,material'], 'wt': ['json'], 'group': ['true'], 'group.field': ['city_pleiades'], 'group.limit': ['-1'], 'q': ['*:* AND display_status:approved'], 'fq': ['(physical_type:"amphora") '], 'facet': ['on'], 'facet.field': ['type', 'physical_type', 'language', 'religion', 'material', 'placeMenu']}
        
        qdict = QueryDict( 'start=0&rows=0&indent=on&fl=inscription_id,region,city,city_geo,notBefore,notAfter,placeMenu,type,physical_type,language,language_display,religion,material&wt=json&group=true&group.field=city_pleiades&group.limit=-1&q=*:* AND display_status:approved&fq=(physical_type:"amphora") &facet=on&facet.field=type&facet.field=physical_type&facet.field=language&facet.field=religion&facet.field=material&facet.field=placeMenu' )
        
        self.assertEqual( 
            'start=0&rows=0&indent=on&fl=inscription_id%2Cregion%2Ccity%2Ccity_geo%2CnotBefore%2CnotAfter%2CplaceMenu%2Ctype%2Cphysical_type%2Clanguage%2Clanguage_display%2Creligion%2Cmaterial&wt=json&group=true&group.field=city_pleiades&group.limit=-1&q=%2A%3A%2A+AND+display_status%3Aapproved&fq=%28physical_type%3A%22amphora%22%29+&facet=on&facet.field=type&facet.field=physical_type&facet.field=language&facet.field=religion&facet.field=material&facet.field=placeMenu', 
            validator.convert_post_params_to_querystring( 'iip', qdict ) 
            )

    ## end class ValidateParamsTest()


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
