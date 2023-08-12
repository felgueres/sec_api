from . import core_bp
from gpt import gpt
from flask import jsonify, request
from .helpers import get_current_weather
from extra.logger_config import setup_logger
from extra.utils import load_prompt 

logger = setup_logger(__name__)

def handle_securities(q, metadata=None):
    prompt = load_prompt('extract_params')['weather']['prompt'].format(q=q)
    pred_location = gpt(prompt=prompt)["choices"][0]["message"]["content"]
    if pred_location == 'locale': pred_location = 'SF' #TODO: get locale from request
    cur_weather_data = get_current_weather(pred_location) 
    return jsonify({'object': 'WeatherWidget', 'data': cur_weather_data}), 200

def handle_no_match(_):
    return jsonify({'object': 'UnknownWidget', 'data': {}}), 200

match_fn = {
    'securities': handle_securities,
    'none': handle_no_match 
}

@core_bp.route('/v1/search', methods=['POST', 'GET'])
def search():
    q = request.args.get('q')
    prompt = load_prompt('classifier')['prompt'].format(q=q, categories=match_fn.keys())
    pred_widget_cls = gpt(prompt=prompt)["choices"][0]["message"]["content"]
    return match_fn[pred_widget_cls](q)
