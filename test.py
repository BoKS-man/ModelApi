from . import utils
from flask import request
from .exception import ApiException
from .api import ModelApi
from .processing import ModelProcess
from .storage import MockMinio

config_path = 'config.yaml'
config = utils.read_config(config_path)

def process():
    try:
        data = utils.check_json(request.json, config['data_template'])
        return model_process.start(data)
    except ApiException as e:
        return e.response
    except Exception as e:
        return utils.prepare_response(e, 500)

def inference(*args, **kwargs):
    pass

if __name__ == "__main__":
    model = None
    storage = MockMinio(utils.update_minio_params(config['minio_params_template'], 'MINIO'))
    model_process = ModelProcess(model, inference, storage, config['exp_root'], config['images_dir_name'])
    api = ModelApi(__name__)
    api.add_endpoint('/process', process, ['POST'])
    api.app.run(host='0.0.0.0', port=utils.update_port(config['default_port']))
