"""
Test module for CodeBuild CDK Constructs
"""

from abc import ABC
from typing import Dict, List, Optional
from os import path

from aws_cdk import (
    aws_codebuild as codebuild,
    aws_iam as iam,
    core
)

from hatch_cdk_constructs.constants import CodeArtifactConstants

DEFAULT_BUILD_ENVIRONMENT = codebuild.BuildEnvironment(
    build_image=codebuild.LinuxBuildImage.STANDARD_4_0,
)


# pylint: disable=too-many-ancestors
class PythonBuildProject(ABC, codebuild.PipelineProject):
    """
    CodeBuild project that builds a default python package.
    """

    # pylint: disable=too-many-arguments
    def __init__(self,
                 scope: core.Construct,
                 name: str,
                 artifact_repository: str = CodeArtifactConstants.CORE_REPOSITORY,
                 domain: str = CodeArtifactConstants.DOMAIN,
                 domain_owner_account_id: str = CodeArtifactConstants.AWS_ACCOUNT_ID,
                 add_install_commands: List[str] = None,
                 test_commands: List[str] = None,
                 build_commands: List[str] = None,
                 post_build_commands: List[str] = None,
                 artifacts: dict = None,
                 environment: codebuild.BuildEnvironment = DEFAULT_BUILD_ENVIRONMENT,
                 runtime_versions: Dict[str, str] = None,
                 **kwargs):

        install_commands = [
            'apt-get update',
            'npm install -g aws-cdk',
            'pip install -U awscli pip pipenv twine wheel',
            f'aws codeartifact login --tool pip --domain {domain} --domain-owner {domain_owner_account_id} '
            f'--repository {artifact_repository}'
        ]

        if runtime_versions is None:
            runtime_versions = {'python': '3.8'}
        if add_install_commands is not None:
            install_commands += add_install_commands

        super().__init__(
            scope,
            name,
            build_spec=codebuild.BuildSpec.from_object({
                'version': '0.2',
                'phases': {
                    'install': {
                        'commands': install_commands,
                        'runtime_versions': runtime_versions,
                    },
                    'pre_build': {
                        'commands': test_commands,
                    },
                    'build': {
                        'commands': build_commands,
                    },
                    'post_build': {
                        'commands': post_build_commands,
                    },
                },
                'artifacts': artifacts,
            }),
            environment=environment,
            **kwargs
        )

        self.role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name('AWSCodeArtifactAdminAccess'))


class PythonWheelBuildProject(PythonBuildProject):
    """
    CodeBuild project that builds a CodeArtifact python package.
    """

    # pylint: disable=too-many-arguments
    def __init__(self,
                 scope: core.Construct,
                 name: str,
                 artifact_repository: str = CodeArtifactConstants.CORE_REPOSITORY,
                 domain: str = CodeArtifactConstants.DOMAIN,
                 domain_owner_account_id: str = CodeArtifactConstants.AWS_ACCOUNT_ID,
                 add_install_commands: Optional[List[str]] = None,
                 test_commands: Optional[List[str]] = None,
                 build_commands: Optional[List[str]] = None,
                 post_build_commands: Optional[List[str]] = None,
                 **kwargs):

        install_commands = [
            f'aws codeartifact login --tool twine --domain {domain} --domain-owner {domain_owner_account_id} '
            f'--repository {artifact_repository}',
            'pip install -r requirements.txt' if path.exists('requirements.txt') else 'pip install .',
        ]

        if add_install_commands is not None:
            install_commands = install_commands + add_install_commands

        if test_commands is None:
            test_commands = [
                'python setup.py test',
            ]
        if build_commands is None:
            build_commands = [
                'python setup.py bdist_wheel',
            ]
        if post_build_commands is None:
            post_build_commands = [
                'twine upload --verbose --repository codeartifact ./dist/*.whl',
            ]

        super().__init__(
            scope=scope,
            name=name,
            domain=domain,
            domain_owner_account_id=domain_owner_account_id,
            artifact_repository=artifact_repository,
            add_install_commands=install_commands,
            test_commands=test_commands,
            build_commands=build_commands,
            post_build_commands=post_build_commands,
            **kwargs
        )
