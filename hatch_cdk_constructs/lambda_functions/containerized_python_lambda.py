"""
Module for containerize lambda function
"""
import os
import subprocess
from pathlib import Path
from shutil import copyfile, copytree
from typing import List, Optional, Set

from aws_cdk import (
    core,
    aws_lambda as lambda_,
)


class ContainerizedPythonLambda(lambda_.DockerImageFunction):
    """
    A Lambda function construct generated using a docker container.
    """

    DOCKER_TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dockerfiles')
    PYTHON_CDK_DOCKERFILE = os.path.join(DOCKER_TEMPLATES_DIR, "PythonCDKDockerfile")
    DOCKER_IGNORE = os.path.join(DOCKER_TEMPLATES_DIR, "dockerignore")

    # Docker build args
    PYTHON_VERSION_ARG = "PYTHON_VERSION"
    INDEX_URL_ARG = "INDEX_URL"
    DEPENDENCIES_ARG = "DEPENDENCIES"

    # pylint: disable=too-few-public-methods
    class PythonVersion:
        """
        Python versions supported by this lambda
        """
        PYTHON_3_8 = '3.8'
        PYTHON_3_7 = '3.7'
        PYTHON_3_6 = '3.6'

    # pylint: disable=too-many-arguments
    def __init__(self, scope: core.Construct, construct_id: str, handler: str, sources: Optional[List[str]] = None,
                 dependencies: Optional[List[str]] = None, python_version: PythonVersion = PythonVersion.PYTHON_3_7,
                 **kwargs):
        """
        Creates a python lambda function using a docker image. Pip must be configured with the proper global index
        url before deploying with CDK. If sources are specifies, these local directories will be copied into the docker
        container and override any modules referring to it.
        """

        build_args = {
            self.PYTHON_VERSION_ARG: python_version,
            self.INDEX_URL_ARG: ContainerizedPythonLambda.get_index_url(),
            self.DEPENDENCIES_ARG: " ".join(ContainerizedPythonLambda.deduplicate_dependencies(sources, dependencies))
        }

        build_directory = ContainerizedPythonLambda.stage_build_artifacts(sources=sources)

        code = lambda_.DockerImageCode.from_image_asset(directory=build_directory.as_posix(),
                                                        cmd=[handler],
                                                        build_args=build_args)

        super().__init__(scope, construct_id, code=code, **kwargs)

    @staticmethod
    def stage_build_artifacts(sources: List[str]) -> Path:
        """
        Stages a clean build directory with the required Dockerfile and local source packages.
        """
        docker_build_dir = Path(core.FileSystem.mkdtemp(prefix='docker-lambda'))

        copyfile(ContainerizedPythonLambda.PYTHON_CDK_DOCKERFILE, os.path.join(docker_build_dir, 'Dockerfile'))
        copyfile(ContainerizedPythonLambda.DOCKER_IGNORE, os.path.join(docker_build_dir, '.dockerignore'))

        for source in sources:
            path = Path(source)
            copytree(path, os.path.join(docker_build_dir, path.name))

        return docker_build_dir

    @staticmethod
    def deduplicate_dependencies(sources: Optional[List[str]] = None,
                                 dependencies: Optional[List[str]] = None) -> Set[str]:
        """
        De-duplicates sources and dependencies, returning only dependencies not found in sources. This allows for
        packages under local development to override dependencies.
        """
        local_sources = {Path(source).name.replace('_', '-') for source in sources} if sources is not None else set()
        set_dependencies = set(dependencies) if dependencies is not None else set()
        return set_dependencies - local_sources

    @staticmethod
    def get_index_url() -> str:
        """
        Gets the index url from pip config. This should be set to retrieve packages from CodeArtifact.
        """
        return subprocess.check_output('echo $(pip config get global.index-url)', shell=True).decode()
