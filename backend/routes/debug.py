"""
Contains the blueprints for routes that are used for testing and debugging.

These routes should be disabled in the production environment, perhaps using
and environment variable to enabled/disabled them?
"""
import logging
from flask import Blueprint, request
from backend.util import http_errors

blueprint = Blueprint('debug', 'debug')


@blueprint.get('/echo')
def echo():
    """
    Echo an input
    """
    try:
        value = request.args['value']
    except KeyError:
        raise http_errors.BadRequest('echo route requires a `value` argument')

    logging.debug('ECHO', value)
    return {'value': value}


@blueprint.post('/clear')
def clear():
    """
    Clear the database
    """
    # TODO
    return {}


@blueprint.post('/shutdown')
def shutdown():
    """
    Initiate a server shutdown
    """
    print("Initiated server shutdown")
    return {}
