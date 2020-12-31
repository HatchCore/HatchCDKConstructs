"""
Module for Python Lambda CDK Constructs
"""
import os
import zipfile

from importlib import util as importlib_util
from typing import List
from uuid import uuid4

from aws_cdk import (
    aws_lambda as lambda_,
    core
)

INIT_FILE_PREFIX = '__init__'
SHARED_OBJECT_EXTENSION = '.so'


class PythonLambdaFunction(lambda_.Function):
    """
    Lambda construct that build its own code package into a zip and uploads it as an s3 asset
    """

    # pylint: disable=too-many-arguments
    def __init__(self, scope: core.Construct, name: str, target_package: str, handler: str,
                 runtime: lambda_.Runtime = lambda_.Runtime.PYTHON_3_8, dependency_packages: List[str] = None,
                 zip_name: str = None, **kwargs):

        code = lambda_.Code.from_asset(self.build_lambda_zip(target_package, dependency_packages, zip_name))
        code.bind(scope)
        super().__init__(scope, name, code=code, handler=handler, runtime=runtime, **kwargs)

    @classmethod
    def build_lambda_zip(cls, target_package: str, dependency_packages: List[str] = None, zip_name: str = None):
        """
        Zips up a target package and specified dependency packages for a lambda handler.
        """
        if dependency_packages is None:
            dependency_packages = []

        if zip_name is None:
            zip_name = f'{str(uuid4())}.zip'

        with zipfile.ZipFile(zip_name, 'w') as lambda_zip:
            cls._add_package_to_zip(lambda_zip, target_package)
            # pylint: disable=expression-not-assigned
            [cls._add_package_to_zip(lambda_zip, dependency_package) for dependency_package in dependency_packages]

        return zip_name

    @staticmethod
    def _add_package_to_zip(lambda_zip: zipfile.ZipFile, package_name: str) -> None:
        package_spec = importlib_util.find_spec(package_name)
        if package_spec is None:
            raise ValueError(f"Package '{package_name}' is not installed in your virtual environment.")
        package_init_path = package_spec.origin
        package_path = os.path.dirname(package_init_path)
        start_path = os.path.dirname(package_path)
        package_init_file_name = os.path.basename(package_init_path)

        if INIT_FILE_PREFIX not in package_init_file_name:
            lambda_zip.write(package_init_path, package_init_file_name)
        else:
            for root, _, files in os.walk(package_path):
                for py_file in files:
                    if SHARED_OBJECT_EXTENSION not in os.path.basename(py_file):
                        abs_path = os.path.join(root, py_file)
                        lambda_zip.write(abs_path, os.path.relpath(abs_path, start_path))
