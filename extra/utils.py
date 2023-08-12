import yaml
import os

def base_dir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_yaml(path): 
    return yaml.safe_load(open(path,'r'))

def join_path(*args):
    return os.path.join(*args)

def load_prompt(fname):
    path = join_path(base_dir(), 'prompts', fname+'.yaml')
    return load_yaml(path)
