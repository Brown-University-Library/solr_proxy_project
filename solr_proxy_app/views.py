import datetime, json, logging, pprint

import requests
from django.conf import settings as project_settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from solr_proxy_app.lib import validator, version_helper

log = logging.getLogger(__name__)


# -------------------------------------------------------------------
# main urls
# -------------------------------------------------------------------


@csrf_exempt
def handler( request, core: str ):
    log.debug( f'\n\nstarting handler; request, ``{pprint.pformat(request.__dict__)}``; core, ``{core}``' )
    ## validate and clean params ------------------------------------
    log.debug( f'method, ``{request.method}``' )
    if request.method == 'POST':
        log.debug( 'hereA' )
        log.debug( f'post, ``{pprint.pformat(request.POST)}``' )
        log.debug( 'hereB' )
    if request.method != 'GET':
        return HttpResponseBadRequest( '400 / Bad Request' )
    core_is_valid: bool = validator.check_core( core )
    if not core_is_valid:
        return HttpResponseNotFound( '404 / Not Found' )
    querystring: str = request.META['QUERY_STRING']
    log.debug( f'querystring, ``{querystring}``')
    ok_params: dict = validator.get_legit_params( core, querystring )
    cleaned_url: str = validator.create_cleaned_url( core, ok_params )
    ## access solr --------------------------------------------------
    resp = requests.get( cleaned_url )
    log.debug( f'resp, ``{pprint.pformat(resp.__dict__)}``' )
    ## build response -----------------------------------------------
    output = resp.content.decode( 'utf-8', 'replace' )
    content_type = 'text/plain; charset=utf-8'
    format_pref = request.GET.get( u'wt', None )
    if format_pref:
        if format_pref == 'json':
            content_type = 'application/json; charset=utf-8'
        elif format_pref == 'xml':
            content_type = 'text/xml; charset=utf-8'
        else:
            content_type = 'text/plain; charset=utf-8'
    # return HttpResponse( f'``{core}`` handling coming' )
    return HttpResponse( output, content_type=content_type )


def info(request):
    return HttpResponse( "Hello, world." )


# -------------------------------------------------------------------
# support urls
# -------------------------------------------------------------------


def error_check( request ):
    """ For an easy way to check that admins receive error-emails (in development)...
        To view error-emails in runserver-development:
        - run, in another terminal window: `python -m smtpd -n -c DebuggingServer localhost:1026`,
        - (or substitue your own settings for localhost:1026)
    """
    log.debug( f'project_settings.DEBUG, ``{project_settings.DEBUG}``' )
    if project_settings.DEBUG == True:
        log.debug( 'triggering exception' )
        raise Exception( 'Raising intentional exception.' )
    else:
        log.debug( 'returing 404' )
        return HttpResponseNotFound( '<div>404 / Not Found</div>' )


def version( request ):
    """ Returns basic branch and commit data. """
    rq_now = datetime.datetime.now()
    commit = version_helper.get_commit()
    branch = version_helper.get_branch()
    info_txt = commit.replace( 'commit', branch )
    context = version_helper.make_context( request, rq_now, info_txt )
    output = json.dumps( context, sort_keys=True, indent=2 )
    log.debug( f'output, ``{output}``' )
    return HttpResponse( output, content_type='application/json; charset=utf-8' )


def root( request ):
    return HttpResponseRedirect( reverse('info_url') )
