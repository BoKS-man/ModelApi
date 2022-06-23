
import os
import glob
import shutil
from minio import Minio
from .exception import ApiException

class MockMinio(Minio):
    def __init__(self, *args, **kwargs):
        pass

    @property
    def url(self):
        return 'fakeurl:9000'

    def check_bucket(self, *args, **kwargs):
        return ['fakeobj']

    def clear_bucket(self, *args, **kwargs):
        pass

    def download(self, local_path, *args, **kwargs):
        with open(os.path.join(local_path, 'fakefile'), 'w') as f:
            f.write('fake!!!')

    def upload(self, *args, **kwargs):
        pass

    def put_object(self, *args, **kwargs):
        pass


class MyMinio(Minio):
    def __init__(self, params:dict):
        super().__init__(params['host'], params['user'], params['password'], secure=params['secure'])

    @property
    def url(self):
        return f'{self._base_url._url.scheme}://{self._base_url.host}'

    def check_bucket(self, name, prefix=None):
        if not self.bucket_exists(name):
            self.make_bucket(name)
            return []
        return [obj.object_name for obj in self.list_objects(name, prefix)]

    def clear_bucket(self, name, prefix=None):
        for obj in self.list_objects(name, prefix):
            self.remove_object(obj.bucket_name, obj.object_name)

    def download(self, local_path, bucket_name, prefix, drop=False):
        files = [o.object_name.replace(bucket_name + '/', '') for o \
            in self.list_objects(bucket_name, prefix + '/', recursive=True)]
        if len(files) == 0:
            raise ApiException(f'There is no files in {os.path.join(self.url, bucket_name, prefix)}', 400)
        for file in files:
            self.fget_object(bucket_name, file, os.path.join(local_path, file.replace(prefix + '/', '')))
        if drop:
            self.clear_bucket(bucket_name, prefix + '/')

    def upload(self, local_path, bucket_name, prefix, drop=False):
        for root, _, files in os.walk(local_path):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as fp:
                    self.put_object(bucket_name, prefix + file_path.replace(local_path, ''), \
                        fp, os.fstat(fp.fileno()).st_size)
        if drop:
            files = glob.glob(os.path.join(local_path, '*'))
            for file_path in files:
                if os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                else:
                    os.remove(file_path)