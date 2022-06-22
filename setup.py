from setuptools import setup

setup(name='modelApi',
      version='0.0.1',
      description='web service for neuristix models',
      install_requires = [
          'flask==2.0.3',
          'pathlib2==2.3.7.post1',
          'minio==7.1.9',
          'json5==0.9.5'],
      packages=['modelApi'])
