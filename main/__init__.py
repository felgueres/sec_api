from flask import Blueprint

core_bp = Blueprint('widgets', __name__, url_prefix='/')

from . import core 