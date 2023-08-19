from . import core_bp
from gpt import gpt
from flask import jsonify, request
from .helpers import get_securities_data
from extra.logger_config import setup_logger
from extra.utils import load_prompt 
from fetchers.sec_facts import get_company_facts
from fetchers.sec_forms import get_latest_10K_url, get_form_text

logger = setup_logger(__name__)

def handle_securities(q):
    # prompt = load_prompt('extract_params')['securities']['prompt'].format(q=q)
    # params = gpt(prompt=prompt)["choices"][0]["message"]["content"]
    # params = get_securities_data(params) 
    out = { 'symbol': 'AirBnb', 'period': None, 'name': 'AirBnb'} 
    cik = 1559720
    facts = get_company_facts(cik, start_date=2020, end_date=2023)
    return jsonify({'object': 'SecuritiesWidget', 'query_params': out, 'facts': facts}), 200

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