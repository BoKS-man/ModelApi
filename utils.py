import os
import yaml
import json
import shutil
from flask import Response
from .exception import ApiException

def prepare_response(message:str=None, status:int=200):
    message = json.dumps({'error': status!=200, 'data': str(message)})
    return Response(message, status)

def check_json(data, template):
    if data is None:
        return template
    if not all([k in list(data.keys()) for k in template.keys()]):
        raise ApiException('Input json must contain keys ' + ','.join(list(template.keys())), 400)
    if not all([(data[k] is not None and isinstance(data[k], str)) for k in template.keys()]):
        raise ApiException('Input json must contain only string values', 400)
    return data

def update_minio_params(template, prefix):
    env_keys = os.environ.keys()
    for env_name, temp_name in zip(['_'.join([prefix, k.upper()]) for k in template.keys()], template.keys()):
        if env_name in env_keys:
            template[temp_name] = os.environ[env_name]
    return template

def update_port(port):
    if 'PORT' in os.environ.keys():
        return os.environ['PORT']
    return port

def read_config(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f'Config file with path {path} not found')
    with open(path, 'r') as c:
        config = yaml.safe_load(c)

    return config

def clear_dir(path):
    if not os.path.exists(path):
        return
    if not os.path.isdir(path):
        raise Exception (f'Can\'t clear {path} it\'s not a directory')
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}: {e}')