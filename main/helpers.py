from dotenv import load_dotenv
import json

load_dotenv()

def get_securities_data(res):
    out = { 'symbol': None, 'period': None, 'name': None } 
    try:
        res = json.loads(res) 
        out['symbol'] = res['symbol']
        out['period'] = res['period']
        out['name'] = res['name']
        return out
    except Exception as e:
        return out 