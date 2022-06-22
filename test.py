import utils
from flask import request
from exception import ApiException

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


app = Flask(__name__)

# initial data. can be set by config file
minio_params_template = {'host': 'localhost:9000',
                         'user': 'admin',
                         'password': 'eFemBOjlrf'}
data_template = {'input': 'images',
                 'output': 'results',
                 'batch_id': 'test'}
weights_path = '/home/appuser/auto_seg/vehicle_crop_v1_b83ee3.pkl'
exp_root = '/home/appuser/results'
images_dir_name = 'images'
model_process = None
default_port = 5001

@app.route('/ping', methods=['GET', 'POST'])
def ping():
    return 'Pong!!!'

@app.route('/process', methods=['GET', 'POST'])


if __name__ == "__main__":
    model_process = ModelProcess(weights_path, update_minio_params(minio_params_template, 'MINIO'), exp_root, images_dir_name)
    app.run(host='0.0.0.0', port=update_port(default_port))
