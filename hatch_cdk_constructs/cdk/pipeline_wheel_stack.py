"""Python wheel hub pipeline stack for PipelineWheelStack"""

from aws_cdk import core

from hatch_cdk_constructs.constructs.code_build import PythonWheelBuildProject
from hatch_cdk_constructs.constructs.code_pipeline import CodeCommitBuildPipeline
from hatch_cdk_constructs.constructs.stacks import PrefixedStack


class PipelineWheelStack(PrefixedStack):
    """
    CloudFormation stack which manages all build and release pipelines for various Python packages.
    """

    def __init__(self,
                 scope: core.Construct,
                 name: str,
                 package_name: str):
        super().__init__(scope, name)

        build_project = PythonWheelBuildProject(scope=self,
                                                name=self._get_prefixed_name(name))

        CodeCommitBuildPipeline(scope=self,
                                name=self._get_prefixed_name(f"{package_name}-WheelPipeline"),
                                source_repository_name=package_name,
                                build_project=build_project)
