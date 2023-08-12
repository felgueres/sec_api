import os 
from bs4.element import Comment
import pandas as pd
import json
from jinja2 import Template

def src_path():
    utils_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(utils_path)

def join_path(source_path, sub_path):
    return os.path.join(source_path, sub_path)

def query_dir_path():
    return join_path(src_path(), 'queries')

def list_dir(dirname):
    return os.listdir(join_path(src_path(), dirname))

def string_formatter(base_string, params):
    return base_string.format(**params)

def is_html_tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]'] or isinstance(element, Comment):
        return False
    return True

def sanitize_CIK(CIK):
   CIK_str = str(CIK)
   missing_zeros = 10 - len(CIK_str) 
   return str(0)  * missing_zeros + CIK_str

def remove_left_zeros(number_str):
    if number_str[0] == '0':
        return remove_left_zeros(number_str[1:])
    else:
        return number_str

def read_word_classifier(classification):
    '''Takes any of the following classes: ['Negative', 'Positive', 'Uncertainty']
    Returns the word list corresponding to that category.
    '''
    if classification not in ['Negative', 'Positive', 'Uncertainty']:
        raise WrongClassification('Must be negative, positive or uncertain')
    base_cols = ['Word']
    df = pd.read_csv(join_path(join_path(src_path(), 'data'),'resources/LoughranMcDonald_MasterDictionary_2020.csv'))
    df = df.loc[df[classification] > 0].copy()
    df = df[base_cols].copy()
    return df['Word'].to_list()

class WrongClassification(Exception):
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message

def read_json(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data

def read_file(path):
    with open(path, 'r') as f:
        c = f.read()
    return c

def str2dict(str):
    return json.loads(str)

def compose_query(q, params):
    '''returns parametrized jinja2 query as json
    '''
    return str2dict(Template(q).render(**params))

def submissions_url(cik):
    return f'https://data.sec.gov/submissions/CIK{cik}.json'
