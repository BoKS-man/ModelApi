import os
from pathlib import Path
from storage import MyMinio
from exception import ApiException
from utils import prepare_response

class ModelProcess():
    def __init__(self, model_weihgts_path:str, \
        minio_params:dict, exp_root:str, images_dir_name:str):
        self.__json_name = 'pipeline_results.json'
        self.__minio = MyMinio(minio_params)
        self.__exp_root = exp_root
        self.__images_dir_name = images_dir_name
        self.__clear_bucket = False
        self.__model = build_car_cropper(model_weihgts_path)

    def start(self, data):
        data = self.__check_data(data)
        if any([k == 'clear' for k in data.keys()]) and data['clear']:
            self.__clear_bucket = True
        else:
            self.__clear_bucket = False
        if data['batch_id'] + '/' in self.__minio.check_bucket(data['output']):
            self.__minio.download(os.path.join(self.__exp_root), data['output'], data['batch_id'])
        else:
            self.__minio.download(os.path.join(self.__exp_root, self.__images_dir_name), data['input'], \
                data['batch_id'], self.__clear_bucket)
        form_crops_for_images(Path(self.__exp_root), None, self.__images_dir_name, self.__model)
        return self.get_result()

    @property
    def minio(self):
        return self.__minio

    @property
    @minio.setter
    def minio(self, value:MyMinio):
        self.__minio = value

    def get_result(self):
        result_path = os.path.join(self.__exp_root, self.__json_name)
        minio_result_name = self.__batch_id + '_auto-seg_result.json'
        with open(result_path, 'rb') as r:
            self.__minio.put_object(self.__output_bucket, minio_result_name, r, os.fstat(r.fileno()).st_size)
        self.__minio.upload(self.__exp_root, self.__output_bucket, self.__batch_id, True)
        if self.__clear_bucket:
            self.__minio.clear_bucket(self.__input_bucket, self.__batch_id + '/')
        return prepare_response(os.path.join(self.__minio.url, self.__output_bucket, minio_result_name))

    def __check_data(self, data):
        self.__input_bucket = data['input']
        self.__output_bucket = data['output']
        self.__batch_id = data['batch_id']
        if len(self.__minio.check_bucket(self.__input_bucket, self.__batch_id + '/')) == 0:
            raise ApiException(f'Input bucket ({os.path.join(self.__input_bucket, self.__batch_id)}) is empty', status=400)
        self.__minio.check_bucket(self.__output_bucket)
        return data


