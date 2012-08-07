"""Blueprint for version 1 of API.
"""
# Fix paths for imports for production deployment
import flask

from akanda.routerapi.drivers import ifconfig


blueprint = flask.Blueprint('v1', __name__)


## APIs for working with system.


@blueprint.route('/system/get_interfaces')
def get_interfaces():
    return 'OpenBSD ifconfig -a'


## APIs for working with firewall.


@blueprint.route('/firewall/get_rules')
def get_rules():
    pass
